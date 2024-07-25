from django.shortcuts import render

# Create your views here.
import httpx
from datetime import datetime
from json import dumps
from random import choice
from string import ascii_letters, digits
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import WarpForm

def genString(stringLength):
    letters = ascii_letters + digits
    return ''.join(choice(letters) for _ in range(stringLength))

def digitString(stringLength):
    digit = digits
    return ''.join(choice(digit) for _ in range(stringLength))

class WarpView(View):
    def get(self, request):
        form = WarpForm()
        return render(request, 'warp.html', {'form': form})

    def post(self, request):
        form = WarpForm(request.POST)
        if form.is_valid():
            warp_client_id = form.cleaned_data['warp_client_id']
            gb_to_add = form.cleaned_data['gb_to_add']

            # Calculate total GB to add (in increments of 5GB)
            total_gb_to_add = gb_to_add 

            SUCCESS_COUNT, FAIL_COUNT = 0, 0

            url = f"https://api.cloudflareclient.com/v0a{digitString(3)}/reg"

            while SUCCESS_COUNT < total_gb_to_add:
                try:
                    install_id = genString(22)
                    body = {
                        "key": f"{genString(43)}=",
                        "install_id": install_id,
                        "fcm_token": f"{install_id}:APA91b{genString(134)}",
                        "referrer": warp_client_id,
                        "warp_enabled": False,
                        "tos": f"{datetime.now().isoformat()[:-3]}+02:00",
                        "type": "Android",
                        "locale": "es_ES"
                    }
                    data = dumps(body).encode("utf8")
                    headers = {
                        "Content-Type": "application/json; charset=UTF-8",
                        "Host": "api.cloudflareclient.com",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                        "User-Agent": "okhttp/3.12.1"
                    }
                    response = httpx.post(url, data=data, headers=headers).status_code
                except Exception as error_code:
                    return JsonResponse({'error': str(error_code)}, status=500)

                if response == 200:
                    SUCCESS_COUNT += 1
                else:
                    FAIL_COUNT += 1

            return JsonResponse({'success': f'{SUCCESS_COUNT}GB added, {FAIL_COUNT} attempts failed.'})
        return render(request, 'warp.html', {'form': form})