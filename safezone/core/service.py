import requests
from datetime import datetime
from typing import Optional, List
from .models import Devices, AccessPasses


class OrangePiClient:
    def __init__(self, *, device_id: int = None, facility_id: int = None, timeout: int = 5):
        if (device_id is None and facility_id is None) or (device_id and facility_id):
            raise ValueError("Укажите либо device_id, либо facility_id, но не оба")

        self.timeout = timeout

        if device_id:
            device = Devices.objects.get(pk=device_id)
            self.devices = [device]
        else:
            self.devices = list(Devices.objects.filter(facility__pk=facility_id))

        if not self.devices:
            raise ValueError("Нет доступных устройств для отправки")

    def send_pass(self, pass_id: int) -> bool:
        access_pass = AccessPasses.objects.filter(pk=pass_id).first()
        if not access_pass:
            return False
        payload = {
            "id": pass_id,
            "qr": access_pass.qr_code_data,
            "valid_from": access_pass.valid_from.isoformat(),
            "valid_to": access_pass.valid_to.isoformat()
        }

        all_success = True
        for device in self.devices:
            url = f"{device.api_url}/api/passes/"
            headers = {
                'Authorization': f'Token {device.api_token}',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"[SEND ERROR] {e} — устройство {device.pk}")
                all_success = False

        if not all_success:
            self.delete_pass(pass_id)
        return all_success

    def delete_pass(self, pass_id: int) -> bool:
        all_success = True
        for device in self.devices:
            url = f"{device.api_url}/api/passes/{pass_id}/"
            headers = {
                'Authorization': f'Token {device.api_token}',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.delete(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"[DELETE ERROR] {e} — устройство {device.pk}")
                all_success = False

        return all_success

    def get_logs(self, start: datetime, end: datetime) -> List[dict]:
        all_logs = []
        params = {
            "start": start.isoformat(),
            "end": end.isoformat()
        }

        for device in self.devices:
            url = f"{device.api_url}/api/logs/"
            headers = {
                'Authorization': f'Token {device.api_token}',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
                response.raise_for_status()
                logs = response.json()
                for log in logs:
                    log['device_id'] = device.pk  # опционально помечаем откуда лог
                all_logs.extend(logs)
            except requests.RequestException as e:
                print(f"[LOGS ERROR] {e} — устройство {device.pk}")

        return all_logs
