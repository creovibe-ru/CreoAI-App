# Происхождение кода

Creo AI — форк открытого проекта [Aether](https://github.com/Zhou-Shilin/Aether).

| | |
|---|---|
| Апстрим | `https://github.com/Zhou-Shilin/Aether` |
| База | коммит `b6681b8` (тег `2.1.7`), ветка `main`, зафиксирован 2026-11-10 |
| Лицензия | GPL-3.0 (см. `LICENSE`, `THIRD_PARTY_NOTICES.md`) |
| Зеркало апстрима | `/opt/creoapp/upstream/Aether` (100% исходник, не изменять) |
| Проверка обновлений | `/opt/creoapp/scripts/upstream-check.sh` |

## Что изменено относительно апстрима

- Ребрендинг: Aether → **Creo AI** (все строки 4 локалей, заголовки, уведомления,
  About-экраны, showcase-контент; «Ask Aether» → «Ask Creo», «Спросить Aether» → «Спросить Creo»).
- Тема: фиолетовая палитра → зелёная Creovibe (`#22C55E` / `#16A34A` / `#4ADE80`)
  в Color.kt (4 схемы), захардкоженные акценты в ConversationUi/IosComposeApp/AetherApp
  (user bubble, composer focus), зелёный индикатор drawer, iOS AccentColor `#22C55E`.
- Логотип: сгенерирован «C»-марка (скрипт `scripts/creo_logo.py`); заменены
  `aether_mark.png` (Android + shared composeResources, имена файлов сохранены —
  на них ссылается код и showcase) и `AppIcon-1024.png` (iOS); вектор уведомлений
  `ic_notification_small.xml` — «C» вместо «A».
- Идентификаторы: applicationId `com.baimoqilin.aether` → `com.creoai.app`,
  iOS Bundle ID + все суффиксы, App Group `group.com.creoai.app`, FileProvider
  domain, ISH-домены/очереди. **Namespace `com.zhousl.aether` и имя XCFramework
  `AetherShared` оставлены** — технические имена кода, не пользовательские.
- Ссылки: сайт → https://creovibe.ru, GitHub → creovibe-ru/CreoAI-App,
  privacy → https://creovibe.ru/privacy; AppUpdateManager смотрит на
  creovibe-ru/CreoAI-App (releases + nightly-артефакт `CreoAI-nightly`).
- Автор в About: CreoVibe. Атрибуция Zhou-Shilin сохранена в README/LICENSE/THIRD_PARTY_NOTICES (GPL-3.0).
- Провайдер по умолчанию: в каталог `PiProviderCatalog` добавлен пресет **CreoVibe**
  (`https://app.creovibe.ru/v1`, OpenAI-совместимый, категория Recommended, первым в списке;
  константы `CreoApiBaseUrl`/`CreoApiDefaultModelId`, хелпер `custom()` расширен параметрами).
- Версии: Android 1.0.0 (versionCode 100), iOS MARKETING_VERSION 1.0.0 (build 100).
- `rootProject.name` = CreoAI. Схемы/таргеты Xcode оставлены `Aether` (внутренние имена).

## Намеренно НЕ изменено (внутренние технические имена)

- Пакеты кода `com.zhousl.aether.*`, классы `Aether*` — переименование сотен
  файлов не даёт пользовательской ценности и делает merge апстрима болезненным.
- Пути рантайма `~/.aether`, `/root/.aether`, env `AETHER_*`, имя фреймворка
  `AetherShared`, scheme/таргеты Xcode, `Theme.Aether`, bridge-имена
  (`AetherChromeBridge`, `reportAetherHeight`, `AetherMarkdownHtmlBridge`).
- Каналы уведомлений: видимые имена заменены, ID (`aether_background_runs`) — нет
  (смена ID роняет настройки каналов у уже установленных пользователей).

## Обновление из апстрима

```bash
/opt/creoapp/scripts/upstream-check.sh     # что нового
# перенести изменения в этот репозиторий (merge/cherry-pick/вручную):
git fetch upstream
git cherry-pick <sha>   # или git merge upstream/main + ручное разрешение
/opt/creoapp/scripts/upstream-check.sh --set-base
```

После масштабного ребрендинга автоматический merge почти всегда конфликтует —
переносить изменения точечно и после каждого переноса проверять, не вернул ли
он «Aether»/фиолетовые цвета/старые ID: `git diff --color-words` + grep.

## Сборка после обновлений

Проверять обе платформы: изменения в `shared/src/commonMain` не покрывают
нативные экраны (`app/` и `iosApp/` дублируют часть UI — см. AGENTS.md).
