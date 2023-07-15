from django.apps import AppConfig


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'

    def ready(self):
        from .preload import object_preload, emotion_preload, microexpression_preload, \
            face_preload, gaze_preload, image_caption_preload, fall_preload
        object_preload()
        emotion_preload()
        microexpression_preload()
        face_preload()
        gaze_preload()
        image_caption_preload()
        # fall_preload()
