# Creo AI

**Локальный AI-агент для Android и iOS в стиле creovibe.ru.**

Creo AI — форк открытого проекта [Aether](https://github.com/Zhou-Shilin/Aether)
(автор Shilin «BaimoQilin» Zhou, лицензия GPL-3.0), переделанный под бренд
CreoVibe: зелёная палитра `#22C55E`, новое имя и логотип, собственные
идентификаторы приложения и ссылки.

## Возможности

- Чат с LLM-провайдерами (~35 встроенных: OpenAI, Anthropic, Google, DeepSeek,
  OpenRouter, любой OpenAI-совместимый endpoint и др.), стриминг, reasoning-таймлайн.
- Полноценный агентный режим на базе Pi Coding Agent: bash/edit/grep-инструменты,
  сессии, ветвление диалогов, scheduled tasks.
- Локальный Linux-рантайм: Alpine (proot на Android, iSH на iOS) + терминал + браузер.
- Расширения: MCP-адаптер, суб-агенты, веб-доступ; Script Extensions API v2.
- Phone Use (Android, через Shizuku/accessibility), интеграция с файловыми
  менеджерами систем (SAF / FileProvider).

## Структура

| Каталог | Назначение |
|---|---|
| `app/` | Android-приложение (Compose) |
| `shared/` | Kotlin Multiplatform: общие данные, UI-компоненты, iOS-хосты |
| `iosApp/` | Xcode-проект (SwiftUI + Compose), FileProvider, iSH-рантайм |
| `pi-bridge/` | TypeScript-мост к Pi Coding Agent (Node 22.19, esbuild) |
| `extensions/` | предустановленные расширения (pi-mcp-adapter, pi-subagents, pi-web-access) |
| `third_party/` | `ish-arm64` (сабмодуль), `termux` (vendored) |
| `spec/`, `docs/`, `design/` | спецификации и внутренняя документация |

## Идентификаторы

| | |
|---|---|
| Android applicationId | `com.creoai.app` |
| iOS Bundle ID | `com.creoai.app` |
| App Group (iOS) | `group.com.creoai.app` |
| Версия | 1.0.0 (versionCode 100) |
| Сайт | https://creovibe.ru |
| API приложения | https://app.creovibe.ru/v1 (провайдер CreoVibe, OpenAI-совместимый) |
| Privacy | https://app.creovibe.ru/privacy |

Kotlin-namespace остаётся `com.zhousl.aether` (техническое имя пакетов кода,
не видно пользователю; сохранено для упрощения синхронизации с апстримом).

## Сборка

### Android

Требуется JDK 17, Android SDK (compileSdk 36, NDK 27), Node.js 22.19.

```bash
git submodule update --init --recursive
./gradlew :app:assembleDebug
```

### iOS

Требуется macOS, Xcode 16+, XcodeGen, JDK 17, Node.js 22.19.

```bash
./scripts/bootstrap-ios.sh   # подготовка рантайма
xcodegen generate            # в iosApp/
```

Team ID передаётся только через параметр `DEVELOPMENT_TEAM=<Team ID>` команды
`xcodebuild`, в репозиторий подписи не коммитятся.

## Синхронизация с апстримом

Регламент — в `UPSTREAM.md` (в корне репозитория развертывания
`/opt/creoapp/UPSTREAM.md`). Проверка обновлений:

```bash
/opt/creoapp/scripts/upstream-check.sh
```

## Лицензия и аттрибуция

Creo AI распространяется под **GPL-3.0** (см. `LICENSE`).
Основано на проекте [Aether](https://github.com/Zhou-Shilin/Aether)
© Shilin Zhou; сторонние компоненты — см. `THIRD_PARTY_NOTICES.md`.
Если APK/IPA передаётся за пределы команды, исходники этого репозитория
должны быть публично доступны (требование GPL-3.0).
