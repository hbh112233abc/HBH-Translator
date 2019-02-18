import sublime
import sublime_plugin
from .driver.baidu_translate import BaiduTranslate

s = sublime.load_settings("HBH-Translator.sublime-settings")
appid = s.get('appid')
secret_key = s.get('secret_key')
print(appid, secret_key)
bd_api = BaiduTranslate(appid, secret_key)


class TranslateCommand(sublime_plugin.TextCommand):
    def run(self, edit, to_lang=''):
        sublime.status_message('Translate...')
        sels = self.view.sel()
        sels_str = []
        for sel in sels:
            sel_str = self.view.substr(sel).strip()
            if sel_str:
                sels_str.append(sel_str)
        print('sels_str:', sels_str)
        if not sels_str:
            sublime.status_message('please select some string to translate!')
            return
        sels_str = '\n'.join(sels_str)
        if to_lang:
            bd_api.to_lang = to_lang
        else:
            bd_api.to_lang = s.get('default_to_lang', 'zh')
        dst = bd_api.query(sels_str)
        sublime.status_message('Translate result:{}'.format(dst))
