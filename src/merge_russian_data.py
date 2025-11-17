"""
Скрипт для объединения русскоязычных сообщений с основным датасетом.

Этот модуль объединяет файл russian_messages.csv с основным raw.csv,
создавая расширенный многоязычный датасет для обучения модели.
"""

import pandas as pd
import os
from pathlib import Path


def merge_datasets():
    """
    Объединяет русскоязычные сообщения с основным датасетом.
    
    Returns:
        pd.DataFrame: Объединенный датасет
    """
    # Пути к файлам
    data_dir = Path(__file__).parent.parent / "data"
    raw_file = data_dir / "raw.csv"
    russian_file = data_dir / "russian_messages.csv"
    output_file = data_dir / "raw_multilingual.csv"
    
    print("📂 Загрузка данных...")
    
    # Загрузка основного датасета (английский)
    df_english = pd.read_csv(raw_file, encoding='latin-1')
    print(f"✓ Загружено английских сообщений: {len(df_english)}")
    
    # Загрузка русскоязычных сообщений
    df_russian = pd.read_csv(russian_file, encoding='utf-8')
    print(f"✓ Загружено русских сообщений: {len(df_russian)}")
    
    # Оставляем только необходимые колонки
    df_english = df_english[['v1', 'v2']].copy()
    df_russian = df_russian[['v1', 'v2']].copy()
    
    # Переименовываем колонки для удобства
    df_english.columns = ['label', 'message']
    df_russian.columns = ['label', 'message']
    
    # Добавляем метку языка
    df_english['language'] = 'en'
    df_russian['language'] = 'ru'
    
    # Объединяем датасеты
    df_combined = pd.concat([df_english, df_russian], ignore_index=True)
    
    # Перемешиваем данные
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Сохраняем результат
    df_combined.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✓ Объединенный датасет сохранен: {output_file}")
    
    # Статистика
    print("\n📊 Статистика объединенного датасета:")
    print(f"   Всего сообщений: {len(df_combined)}")
    print(f"   Спам: {len(df_combined[df_combined['label'] == 'spam'])} ({len(df_combined[df_combined['label'] == 'spam'])/len(df_combined)*100:.1f}%)")
    print(f"   Ham: {len(df_combined[df_combined['label'] == 'ham'])} ({len(df_combined[df_combined['label'] == 'ham'])/len(df_combined)*100:.1f}%)")
    print(f"\n   По языкам:")
    print(f"   Английский: {len(df_combined[df_combined['language'] == 'en'])}")
    print(f"   Русский: {len(df_combined[df_combined['language'] == 'ru'])}")
    
    return df_combined


def create_backup():
    """Создает резервную копию оригинального raw.csv"""
    data_dir = Path(__file__).parent.parent / "data"
    raw_file = data_dir / "raw.csv"
    backup_file = data_dir / "raw_english_only.csv"
    
    if not backup_file.exists():
        df = pd.read_csv(raw_file, encoding='latin-1')
        df.to_csv(backup_file, index=False, encoding='latin-1')
        print(f"✓ Создана резервная копия: {backup_file}")


def update_raw_file():
    """
    Обновляет raw.csv многоязычным датасетом.
    
    ВНИМАНИЕ: Это заменит оригинальный raw.csv!
    """
    data_dir = Path(__file__).parent.parent / "data"
    multilingual_file = data_dir / "raw_multilingual.csv"
    raw_file = data_dir / "raw.csv"
    
    if multilingual_file.exists():
        # Читаем многоязычный датасет
        df = pd.read_csv(multilingual_file, encoding='utf-8')
        
        # Конвертируем в формат оригинального raw.csv
        df_output = pd.DataFrame()
        df_output['v1'] = df['label']
        df_output['v2'] = df['message']
        df_output['v3'] = ''
        df_output['v4'] = ''
        df_output['v5'] = ''
        
        # Сохраняем
        df_output.to_csv(raw_file, index=False, encoding='utf-8')
        print(f"✓ Файл {raw_file} обновлен многоязычными данными")
    else:
        print(f"✗ Файл {multilingual_file} не найден. Сначала выполните merge_datasets()")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("🔄 ОБЪЕДИНЕНИЕ ДАТАСЕТОВ")
    print("=" * 60)
    
    # Создаем резервную копию
    create_backup()
    
    # Объединяем датасеты
    df = merge_datasets()
    
    print("\n" + "=" * 60)
    print("❓ Хотите заменить raw.csv многоязычной версией?")
    print("   Это позволит использовать русские сообщения в обучении.")
    print("   (Оригинал сохранен как raw_english_only.csv)")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--update-raw':
        update_raw_file()
        print("\n✅ Готово! Теперь можно запустить prepare.py и train.py")
    else:
        print("\nДля обновления raw.csv запустите:")
        print("  python src/merge_russian_data.py --update-raw")
