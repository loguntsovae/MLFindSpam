"""
Script for merging Russian language messages with the main dataset.

This module merges the russian_messages.csv file with the main raw.csv,
creating an extended multilingual dataset for model training.
"""

import pandas as pd
from pathlib import Path


def merge_datasets():
    """
    Merges Russian language messages with the main dataset.
    
    Returns:
        pd.DataFrame: Combined dataset
    """
    # File paths
    data_dir = Path(__file__).parent.parent / "data"
    raw_file = data_dir / "raw.csv"
    russian_file = data_dir / "russian_messages.csv"
    output_file = data_dir / "raw_multilingual.csv"
    
    print("📂 Loading data...")
    
    # Load main dataset (English)
    df_english = pd.read_csv(raw_file, encoding='latin-1')
    print(f"✓ Loaded English messages: {len(df_english)}")
    
    # Load Russian language messages
    df_russian = pd.read_csv(russian_file, encoding='utf-8')
    print(f"✓ Loaded Russian messages: {len(df_russian)}")
    
    # Keep only necessary columns
    df_english = df_english[['v1', 'v2']].copy()
    df_russian = df_russian[['v1', 'v2']].copy()
    
    # Rename columns for convenience
    df_english.columns = ['label', 'message']
    df_russian.columns = ['label', 'message']
    
    # Add language label
    df_english['language'] = 'en'
    df_russian['language'] = 'ru'
    
    # Combine datasets
    df_combined = pd.concat([df_english, df_russian], ignore_index=True)
    
    # Shuffle data
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save result
    df_combined.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✓ Combined dataset saved: {output_file}")
    
    # Statistics
    print("\n📊 Combined dataset statistics:")
    print(f"   Total messages: {len(df_combined)}")
    print(f"   Spam: {len(df_combined[df_combined['label'] == 'spam'])} ({len(df_combined[df_combined['label'] == 'spam'])/len(df_combined)*100:.1f}%)")
    print(f"   Ham: {len(df_combined[df_combined['label'] == 'ham'])} ({len(df_combined[df_combined['label'] == 'ham'])/len(df_combined)*100:.1f}%)")
    print(f"\n   By language:")
    print(f"   English: {len(df_combined[df_combined['language'] == 'en'])}")
    print(f"   Russian: {len(df_combined[df_combined['language'] == 'ru'])}")
    
    return df_combined


def create_backup():
    """Creates a backup copy of the original raw.csv"""
    data_dir = Path(__file__).parent.parent / "data"
    raw_file = data_dir / "raw.csv"
    backup_file = data_dir / "raw_english_only.csv"
    
    if not backup_file.exists():
        df = pd.read_csv(raw_file, encoding='latin-1')
        df.to_csv(backup_file, index=False, encoding='latin-1')
        print(f"✓ Backup created: {backup_file}")


def update_raw_file():
    """
    Updates raw.csv with the multilingual dataset.
    
    WARNING: This will replace the original raw.csv!
    """
    data_dir = Path(__file__).parent.parent / "data"
    multilingual_file = data_dir / "raw_multilingual.csv"
    raw_file = data_dir / "raw.csv"
    
    if multilingual_file.exists():
        # Read multilingual dataset
        df = pd.read_csv(multilingual_file, encoding='utf-8')
        
        # Convert to original raw.csv format
        df_output = pd.DataFrame()
        df_output['v1'] = df['label']
        df_output['v2'] = df['message']
        df_output['v3'] = ''
        df_output['v4'] = ''
        df_output['v5'] = ''
        
        # Save
        df_output.to_csv(raw_file, index=False, encoding='utf-8')
        print(f"✓ File {raw_file} updated with multilingual data")
    else:
        print(f"✗ File {multilingual_file} not found. Run merge_datasets() first")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("🔄 DATASET MERGING")
    print("=" * 60)
    
    # Create backup
    create_backup()
    
    # Merge datasets
    df = merge_datasets()
    
    print("\n" + "=" * 60)
    print("❓ Replace raw.csv with multilingual version?")
    print("   This will enable Russian messages in training.")
    print("   (Original saved as raw_english_only.csv)")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--update-raw':
        update_raw_file()
        print("\n✅ Done! Now you can run prepare.py and train_enhanced.py")
    else:
        print("\nTo update raw.csv, run:")
        print("  python src/merge_russian_data.py --update-raw")
