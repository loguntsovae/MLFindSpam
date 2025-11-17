#!/usr/bin/env python3
"""
Simple script to merge Russian and English datasets.
Merges directly into raw.csv for Docker build.
"""

import pandas as pd
from pathlib import Path

# Пути к файлам
data_dir = Path("data")
raw_file = data_dir / "raw.csv"
russian_file = data_dir / "russian_messages.csv"
backup_file = data_dir / "raw_english_only_backup.csv"

print("🔄 Merging datasets...")

# Создаем backup если его еще нет
if not backup_file.exists() and raw_file.exists():
    df_backup = pd.read_csv(raw_file, encoding='latin-1')
    df_backup.to_csv(backup_file, index=False, encoding='latin-1')
    print(f"✓ Backup created: {backup_file}")

# Загружаем английские данные
df_english = pd.read_csv(raw_file, encoding='latin-1')
print(f"✓ English messages: {len(df_english)}")

# Загружаем русские данные
df_russian = pd.read_csv(russian_file, encoding='utf-8')
print(f"✓ Russian messages: {len(df_russian)}")

# Создаем новый датасет в формате raw.csv
df_merged = pd.DataFrame()
df_merged['v1'] = pd.concat([df_english['v1'], df_russian['v1']], ignore_index=True)
df_merged['v2'] = pd.concat([df_english['v2'], df_russian['v2']], ignore_index=True)
df_merged['v3'] = ''
df_merged['v4'] = ''
df_merged['v5'] = ''

# Перемешиваем
df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)

# Сохраняем в UTF-8
df_merged.to_csv(raw_file, index=False, encoding='utf-8')

print(f"\n✅ Merged dataset saved to {raw_file}")
print(f"   Total messages: {len(df_merged)}")
print(f"   Spam: {len(df_merged[df_merged['v1'] == 'spam'])}")
print(f"   Ham: {len(df_merged[df_merged['v1'] == 'ham'])}")
print("\n🚀 Ready to build Docker image!")
