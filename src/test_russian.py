#!/usr/bin/env python3
"""
Demonstration of the model working with Russian language messages.

This script shows examples of classifying Russian SMS messages as spam and ham.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.predict import predict_message, predict_proba


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def test_message(message, expected=None):
    """Test a message and display the result"""
    result = predict_message(message)
    proba = predict_proba(message)
    
    # Choose emoji
    emoji = "❌" if result == "spam" else "✅"
    
    # Format result with color
    result_str = f"{emoji} {result.upper()}"
    
    print(f"\n📱 Message: \"{message}\"")
    print(f"   Result: {result_str}")
    print(f"   Probabilities: HAM={proba['ham']:.2%}, SPAM={proba['spam']:.2%}")
    
    if expected:
        match = "✓" if result == expected else "✗"
        print(f"   Expected: {expected.upper()} {match}")


def main():
    print_header("🇷🇺 RUSSIAN LANGUAGE MODEL TESTING")
    
    print("\n📝 This script demonstrates the model working with Russian language messages.")
    print("   Make sure the model is trained on the multilingual dataset!")
    
    # Check if model exists
    model_path = Path(__file__).parent.parent / "models" / "model.pkl"
    if not model_path.exists():
        print("\n⚠️  WARNING: Model not found!")
        print("   First, train the model:")
        print("   1. python src/merge_russian_data.py --update-raw")
        print("   2. python src/prepare.py")
        print("   3. python src/train_enhanced.py")
        return
    
    # HAM examples
    print_header("✅ HAM EXAMPLES (LEGITIMATE MESSAGES)")
    
    ham_examples = [
        "Привет! Как дела? Когда встретимся?",
        "Встреча перенесена на пятницу в 15:00",
        "Спасибо за помощь, без тебя бы не справился",
        "Завтра в офис можно не приходить, работаем удаленно",
        "Врач сказал что все в порядке, можно не волноваться",
        "Не забудь купить молоко и хлеб по дороге домой",
    ]
    
    for msg in ham_examples:
        test_message(msg, expected="ham")
    
    # SPAM examples
    print_header("❌ SPAM EXAMPLES (FRAUDULENT MESSAGES)")
    
    spam_examples = [
        "СРОЧНО! Вы выиграли iPhone 15 Pro! Для получения приза перейдите по ссылке",
        "ВНИМАНИЕ! Ваша карта заблокирована! Срочно позвоните 8-XXX-XXX-XXXX",
        "Поздравляем! Вам одобрен кредит до 500000 рублей без справок!",
        "Только сегодня! Скидка 90% на все товары! Успей купить!",
        "Заработок от 50000 рублей в день без вложений!",
        "БЕСПЛАТНАЯ раздача денег! Первым 100 участникам по 10000 руб!",
    ]
    
    for msg in spam_examples:
        test_message(msg, expected="spam")
    
    # Edge cases
    print_header("⚠️  EDGE CASES")
    
    edge_cases = [
        "Акция! Скидка 20% по промокоду SUMMER2024 в нашем магазине",
        "Ваш заказ №12345 отправлен. Трек-номер: 123456789",
        "Срочно нужна помощь! Позвони как только сможешь",
        "Напоминание: платеж по кредиту 15 числа",
    ]
    
    for msg in edge_cases:
        test_message(msg)
    
    # Interactive mode
    print_header("🎮 INTERACTIVE MODE")
    print("\nEnter your message to test (or 'exit' to quit):")
    
    while True:
        try:
            user_input = input("\n📱 > ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            test_message(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print_header("✨ TESTING COMPLETE")
    print("\n💡 Tips:")
    print("   • To improve quality, add more examples to russian_messages.csv")
    print("   • Retrain the model after adding new data")
    print("   • Use the web interface: python ui/app.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
