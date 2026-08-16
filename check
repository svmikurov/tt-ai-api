#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

API_URL="http://localhost:8000"
AI_API_URL="http://localhost:8001"

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Проверка системы Tech Task CHKPZ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================
# 1. Проверка здоровья сервисов
# ============================================
echo -e "${BLUE}1. Проверка здоровья сервисов${NC}"
echo "───────────────────────────────────────────────────────"

echo -n "  ${YELLOW}→${NC} Основной API ... "
curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" | grep -q "200" && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ Ошибка${NC}"

echo -n "  ${YELLOW}→${NC} AI API ... "
curl -s -o /dev/null -w "%{http_code}" "$AI_API_URL/health" | grep -q "200" && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ Ошибка${NC}"

echo -n "  ${YELLOW}→${NC} AI API (metrics) ... "
curl -s -o /dev/null -w "%{http_code}" "$AI_API_URL/metrics" | grep -q "200" && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ Ошибка${NC}"

echo -n "  ${YELLOW}→${NC} Redis ... "
redis_response=$(curl -s "$API_URL/redis-check" 2>/dev/null)
echo "$redis_response" | grep -q "connected" && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ Ошибка${NC}"

echo -n "  ${YELLOW}→${NC} PostgreSQL ... "
db_response=$(curl -s "$API_URL/db-check" 2>/dev/null)
echo "$db_response" | grep -q "connected" && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ Ошибка${NC}"

echo ""

# ============================================
# 2. Проверка эндпоинтов
# ============================================
echo -e "${BLUE}2. Проверка эндпоинтов${NC}"
echo "───────────────────────────────────────────────────────"

echo -n "  ${YELLOW}→${NC} Отправка задачи (через API) ... "
response=$(curl -s -X POST "$API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Тест"}' 2>/dev/null)
echo "$response" | grep -q "task_id" && echo -e "${GREEN}✓ OK${NC}" || echo -e "${RED}✗ Ошибка${NC}"

echo -n "  ${YELLOW}→${NC} Прямой вызов AI API ... "
ai_response=$(curl -s -X POST "$AI_API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Тест"}' 2>/dev/null)
if echo "$ai_response" | grep -q "busy"; then
    echo -e "${YELLOW}⚠ Занято (429)${NC}"
else
    echo -e "${GREEN}✓ OK${NC}"
fi

echo ""

# ============================================
# 3. Проверка синхронности AI API (отбрасывание запросов)
# ============================================
echo -e "${BLUE}3. Проверка синхронности AI API (отбрасывание запросов)${NC}"
echo "───────────────────────────────────────────────────────"

echo -n "  ${YELLOW}→${NC} Отправка первого запроса ... "
curl -s -X POST "$AI_API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Долгий запрос"}' > /dev/null &
PID1=$!
echo -e "${GREEN}✓ запущен${NC}"

sleep 1

echo -n "  ${YELLOW}→${NC} Отправка второго запроса (должен быть отклонён) ... "
response2=$(curl -s -X POST "$AI_API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Второй запрос"}' 2>/dev/null)

if echo "$response2" | grep -q "busy"; then
    echo -e "${GREEN}✓ Отклонён (модель занята)${NC}"
else
    echo -e "${YELLOW}⚠ Ответ: $response2${NC}"
fi

# Ждём завершения первого запроса
wait $PID1 2>/dev/null

echo ""

# ============================================
# 4. Документация API
# ============================================
echo -e "${BLUE}4. Документация API${NC}"
echo "───────────────────────────────────────────────────────"
echo -e "  ${YELLOW}→${NC} Swagger UI (API):      ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  ${YELLOW}→${NC} Swagger UI (AI API):   ${GREEN}http://localhost:8001/docs${NC}"

echo ""

# ============================================
# 5. Полный цикл запроса
# ============================================
echo -e "${BLUE}5. Полный цикл запроса${NC}"
echo "───────────────────────────────────────────────────────"

echo -n "  ${YELLOW}→${NC} Отправка запроса: \"Привет, нейросеть! Как дела?\" ... "
response=$(curl -s -X POST "$API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Привет, нейросеть! Как дела?"}' 2>/dev/null)
task_id=$(echo "$response" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)

if [ -n "$task_id" ]; then
    echo -e "${GREEN}✓ Получен task_id: $task_id${NC}"
else
    echo -e "${RED}✗ Не удалось получить task_id${NC}"
    echo "Ответ: $response"
    exit 1
fi

echo -n "  ${YELLOW}→${NC} Ожидание выполнения задачи "
for i in {1..10}; do
    sleep 1
    echo -n "."
done
echo ""

echo -n "  ${YELLOW}→${NC} Получение результата ... "
result=$(curl -s "$API_URL/result/$task_id" 2>/dev/null)
status=$(echo "$result" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ "$status" = "completed" ]; then
    echo -e "${GREEN}✓ Готово${NC}"
    echo ""
    echo -e "${BLUE}  Результат:${NC}"
    echo "$result" | jq '.' 2>/dev/null || echo "$result"
else
    echo -e "${YELLOW}⚠ Статус: $status${NC}"
    echo "$result" | jq '.' 2>/dev/null || echo "$result"
fi

echo ""

# ============================================
# 6. Статистика
# ============================================
echo -e "${BLUE}6. Статистика${NC}"
echo "───────────────────────────────────────────────────────"

echo -n "  ${YELLOW}→${NC} Статус очереди Celery ... "
celery_status=$(curl -s "$API_URL/result/dummy" 2>/dev/null | head -c 50)
if [ -n "$celery_status" ]; then
    echo -e "${GREEN}✓ Доступен${NC}"
else
    echo -e "${RED}✗ Недоступен${NC}"
fi

echo -n "  ${YELLOW}→${NC} Состояние AI API ... "
ai_status=$(curl -s "$AI_API_URL/health" 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$ai_status" = "ok" ]; then
    echo -e "${GREEN}✓ Работает${NC}"
else
    echo -e "${RED}✗ Не работает${NC}"
fi

echo ""

# ============================================
# Итог
# ============================================
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Проверка завершена!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"