#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Базовый URL
API_URL="http://localhost:8000"
AI_API_URL="http://localhost:8001"

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Проверка системы Tech Task CHKPZ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Функция для проверки здоровья
check_health() {
    local name=$1
    local url=$2
    
    echo -n "  ${YELLOW}→${NC} Проверка $name ... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ Ошибка (код: $response)${NC}"
        return 1
    fi
}

# Функция для проверки эндпоинта
check_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    echo -n "  ${YELLOW}→${NC} $description ... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" 2>/dev/null)
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" -H "Content-Type: application/json" -d "$data" 2>/dev/null)
    fi
    
    if [ "$response" = "200" ] || [ "$response" = "201" ]; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    elif [ "$response" = "429" ]; then
        echo -e "${YELLOW}⚠ Занято (429)${NC}"
        return 0
    else
        echo -e "${RED}✗ Ошибка (код: $response)${NC}"
        return 1
    fi
}

# Функция для тестирования полного цикла
test_full_cycle() {
    local query=$1
    
    echo -e "\n${BLUE}--- Тест: Полный цикл запроса ---${NC}"
    
    # 1. Отправляем запрос
    echo -n "  ${YELLOW}→${NC} Отправка запроса: \"$query\" ... "
    
    response=$(curl -s -X POST "$API_URL/predict" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}" 2>/dev/null)
    
    task_id=$(echo "$response" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$task_id" ]; then
        echo -e "${GREEN}✓ Получен task_id: $task_id${NC}"
    else
        echo -e "${RED}✗ Не удалось получить task_id${NC}"
        echo "Ответ: $response"
        return 1
    fi
    
    # 2. Ожидаем выполнения (с анимацией)
    echo -n "  ${YELLOW}→${NC} Ожидание выполнения задачи "
    
    for i in {1..10}; do
        sleep 1
        echo -n "."
    done
    echo ""
    
    # 3. Получаем результат
    echo -n "  ${YELLOW}→${NC} Получение результата ... "
    
    result=$(curl -s "$API_URL/result/$task_id" 2>/dev/null)
    status=$(echo "$result" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ "$status" = "completed" ]; then
        echo -e "${GREEN}✓ Готово${NC}"
        echo ""
        echo -e "${BLUE}  Результат:${NC}"
        echo "$result" | jq '.' 2>/dev/null || echo "$result"
        return 0
    else
        echo -e "${YELLOW}⚠ Статус: $status${NC}"
        echo "$result" | jq '.' 2>/dev/null || echo "$result"
        return 1
    fi
}

# --- Выполнение проверок ---

# 1. Проверка здоровья сервисов
echo -e "${BLUE}1. Проверка здоровья сервисов${NC}"
echo "───────────────────────────────────────────────────────"

check_health "Основной API" "$API_URL/health"
check_health "AI API" "$AI_API_URL/health"
check_health "Детальный статус AI API" "$AI_API_URL/metrics"

echo ""

# 2. Проверка эндпоинтов
echo -e "${BLUE}2. Проверка эндпоинтов${NC}"
echo "───────────────────────────────────────────────────────"

check_endpoint "POST" "$API_URL/predict" '{"query":"Тест"}' "Отправка задачи (через API)"
check_endpoint "POST" "$AI_API_URL/predict" '{"query":"Тест"}' "Прямой вызов AI API"

echo ""

# 3. Проверка отбрасывания запросов (синхронность AI API)
echo -e "${BLUE}3. Проверка синхронности AI API (отбрасывание запросов)${NC}"
echo "───────────────────────────────────────────────────────"

echo -n "  ${YELLOW}→${NC} Отправка первого запроса ... "
curl -s -X POST "$AI_API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Долгий запрос"}' > /dev/null &
PID1=$!
echo -e "${GREEN}✓ запущен${NC}"

sleep 1

echo -n "  ${YELLOW}→${NC} Отправка второго запроса (должен быть отклонён) ... "
response=$(curl -s -X POST "$AI_API_URL/predict" -H "Content-Type: application/json" -d '{"query":"Второй запрос"}' 2>/dev/null)

if echo "$response" | grep -q "busy"; then
    echo -e "${GREEN}✓ Отклонён (модель занята)${NC}"
else
    echo -e "${YELLOW}⚠ Ответ: $response${NC}"
fi

# Ждём завершения первого запроса
wait $PID1 2>/dev/null

echo ""

# 4. Проверка через Swagger UI
echo -e "${BLUE}4. Документация API${NC}"
echo "───────────────────────────────────────────────────────"
echo -e "  ${YELLOW}→${NC} Swagger UI (основной API): ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  ${YELLOW}→${NC} Swagger UI (AI API):      ${GREEN}http://localhost:8001/docs${NC}"

echo ""

# 5. Полный цикл
echo -e "${BLUE}5. Полный цикл запроса${NC}"
echo "───────────────────────────────────────────────────────"

test_full_cycle "Привет, нейросеть! Как дела?"

echo ""

# 6. Статистика
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

# Итог
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Проверка завершена!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"