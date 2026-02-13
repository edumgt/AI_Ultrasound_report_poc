from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST


@require_GET
def index(request: HttpRequest):
    return render(request, "recorder/index.html")


@require_POST
def upload_audio(request: HttpRequest):
    audio_file = request.FILES.get("audio")
    transcript = request.POST.get("transcript", "").strip()

    if audio_file is None:
        return JsonResponse({"ok": False, "error": "audio 파일이 없습니다."}, status=400)

    recordings_dir = Path(settings.BASE_DIR) / "recordings"
    recordings_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}_{audio_file.name}"
    target = recordings_dir / filename

    with target.open("wb") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    return JsonResponse(
        {
            "ok": True,
            "saved_file": str(target.relative_to(settings.BASE_DIR)),
            "transcript": transcript,
            "message": "녹음 파일 업로드 완료",
        }
    )
