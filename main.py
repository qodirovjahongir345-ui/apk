# main.py
# "O'qish taymeri" - vaqt tugamaguncha ekranni qulflab turadigan ilova.
# Ko'rinishi oddiy taymer kabi: katta raqam kiritish maydoni,
# katta Start tugmasi, katta countdown ko'rsatgich.

import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

IS_ANDROID = True
try:
    from jnius import autoclass
except Exception:
    IS_ANDROID = False


def get_activity():
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    return PythonActivity.mActivity


def is_lock_task_active():
    if not IS_ANDROID:
        return False
    try:
        activity = get_activity()
        Context = autoclass('android.content.Context')
        am = activity.getSystemService(Context.ACTIVITY_SERVICE)
        return am.getLockTaskModeState() != 0
    except Exception:
        try:
            activity = get_activity()
            Context = autoclass('android.content.Context')
            am = activity.getSystemService(Context.ACTIVITY_SERVICE)
            return bool(am.isInLockTaskMode())
        except Exception:
            return False


def start_lock_task():
    if not IS_ANDROID:
        return False, "Faqat Android qurilmada ishlaydi."
    try:
        get_activity().startLockTask()
    except Exception as e:
        return False, (
            "Pin yoqilmadi. Sozlamalar -> Xavfsizlik -> "
            "'App pinning' ni yoqing. Xato: %s" % e
        )
    time.sleep(0.3)
    if is_lock_task_active():
        return True, "Qulflandi. O'qishga xush kelibsiz."
    return False, (
        "Pin faollashmadi. Sozlamalar -> Xavfsizlik -> "
        "'App pinning' ni yoqib, qayta urinib ko'ring."
    )


def stop_lock_task():
    if not IS_ANDROID:
        return
    try:
        get_activity().stopLockTask()
    except Exception:
        pass


def keep_screen_on(flag: bool):
    if not IS_ANDROID:
        return
    try:
        activity = get_activity()
        LP = autoclass('android.view.WindowManager$LayoutParams')
        window = activity.getWindow()
        if flag:
            window.addFlags(LP.FLAG_KEEP_SCREEN_ON)
        else:
            window.clearFlags(LP.FLAG_KEEP_SCREEN_ON)
    except Exception:
        pass


BG = (0.07, 0.07, 0.09, 1)
ACCENT = (0.20, 0.55, 0.95, 1)
GREEN = (0.20, 0.75, 0.45, 1)


class TimerRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=40, spacing=25, **kwargs)
        self.remaining = 0
        self.locked = False
        self.event = None
        self.watchdog = None

        with self.canvas.before:
            Color(*BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.status = Label(
            text="O'qish uchun daqiqa kiriting",
            font_size='20sp',
            color=(1, 1, 1, 0.8)
        )
        self.add_widget(self.status)

        self.countdown = Label(
            text="00:00",
            font_size='72sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.countdown)

        self.minutes_input = TextInput(
            text="30",
            input_filter='int',
            multiline=False,
            font_size='34sp',
            halign='center',
            size_hint=(1, 0.18),
            background_color=(1, 1, 1, 0.08),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
        )
        self.add_widget(self.minutes_input)

        self.start_btn = Button(
            text="BOSHLASH",
            font_size='24sp',
            bold=True,
            size_hint=(1, 0.2),
            background_normal='',
            background_color=ACCENT,
            on_press=self.start_session
        )
        self.add_widget(self.start_btn)

        Window.bind(on_keyboard=self.on_key)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_key(self, window, key, *args):
        if self.locked and key == 27:  # Android Back tugmasi
            return True
        return False

    def start_session(self, instance):
        try:
            mins = int(self.minutes_input.text)
        except ValueError:
            mins = 30
        mins = max(mins, 1)

        ok, msg = start_lock_task()
        self.status.text = msg
        if not ok:
            return

        keep_screen_on(True)
        self.locked = True
        self.remaining = mins * 60
        self.start_btn.disabled = True
        self.start_btn.background_color = (0.4, 0.4, 0.4, 1)
        self.minutes_input.disabled = True

        if self.event:
            self.event.cancel()
        self.event = Clock.schedule_interval(self.tick, 1)
        self.watchdog = Clock.schedule_interval(self.check_still_locked, 5)

    def check_still_locked(self, dt):
        if self.locked and IS_ANDROID and not is_lock_task_active():
            start_lock_task()

    def tick(self, dt):
        if self.remaining <= 0:
            self.finish_session()
            return
        self.remaining -= 1
        m, s = divmod(self.remaining, 60)
        self.countdown.text = "%02d:%02d" % (m, s)

    def finish_session(self):
        if self.event:
            self.event.cancel()
            self.event = None
        if self.watchdog:
            self.watchdog.cancel()
            self.watchdog = None
        self.countdown.text = "00:00"
        self.status.text = "Vaqt tugadi!"
        self.locked = False
        self.start_btn.disabled = False
        self.start_btn.background_color = GREEN
        self.minutes_input.disabled = False
        keep_screen_on(False)
        stop_lock_task()


class FocusTimerApp(App):
    def build(self):
        self.title = "O'qish Taymeri"
        return TimerRoot()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    FocusTimerApp().run()
