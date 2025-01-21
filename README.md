# Запись на улугу BODY TOP

## Описание
Fullstack web приложение для создания записи на предлагаемую услугу.

## Стек технологий
- Языки программирования:  Python, JS, HTML&CSS
- Фреймворки: FastAPI, Aiogram, Sqlalchymy, Asyncio
- База данных: PostgreSQL
- Другие технлогии: Git

## Установка и Запуск
### Установка
1. Скопируйте проект.
```bash
git clone https://github.com/ivalukyan/yclients-backend.git
```

2. Перейдите в папку с проектом.
```bash
cd yclients-backend
```

3. Установите докер.
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

4. Проверьте наличие докера.
```bash
docker --version
```

### Запуск
1. Создадим образ докер нашего проекта.
```bash
docker build -t backend .
```

2. Запустим докер образ.
```bash
docker run -d -p 8000:8000 --name yclients-backend backend
```