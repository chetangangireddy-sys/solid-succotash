"""StudySprint - a small flashcard and quiz trainer.

Run it with:  python main.py
"""

import time

import storage
from features import core, reports


def show_menu():
    print()
    print("=== StudySprint ===")
    print("1) Take the quiz")
    print("2) List cards")
    print("3) Add a card")
    print("4) Study a category")
    print("5) Show the last card")
    print("6) Category breakdown")
    print("7) Deck summary")
    print("8) Score summary")
    print("9) Lightning round")
    print("10) Import cards from CSV")
    print("0) Quit")


def main():
    data = storage.load_data()
    while True:
        show_menu()
        try:
            choice = input("Pick an option: ").strip()
        except EOFError:
            print()
            break
        if choice == "0":
            print("See you next session!")
            break
        elif choice in ("1", "9"):
            cards = core.get_cards(data)
            started = time.perf_counter() if choice == "9" else None
            score = core.run_quiz(cards)
            total = len(cards)
            print("You scored " + str(score) + "/" + str(total) +
                  " (" + str(core.percent_correct(score, total)) + "%).")
            if started is not None:
                elapsed = time.perf_counter() - started
                print("Time: " + format(elapsed, ".2f") + " seconds.")
            core.record_score(data, score)
            storage.save_data(data)
        elif choice == "2":
            core.list_cards(core.get_cards(data))
        elif choice == "3":
            question = input("Question: ")
            answer = input("Answer: ")
            core.add_card(data, question, answer)
            storage.save_data(data)
            print("Card added.")
        elif choice == "4":
            category = input("Category: ").strip()
            matches = core.cards_by_category(core.get_cards(data), category)
            if matches:
                for card in matches:
                    print("- " + card["question"])
            else:
                print("No cards found in that category.")
        elif choice == "5":
            cards = core.get_cards(data)
            if cards:
                print(core.top_card(cards)["question"])
            else:
                print("The deck has no cards yet.")
        elif choice == "6":
            print(reports.category_report(data))
        elif choice == "7":
            print(reports.deck_summary(data))
        elif choice == "8":
            print(reports.score_summary(data))
        elif choice == "10":
            path = input("CSV file path: ").strip()
            try:
                imported = core.import_cards_from_csv(path, core.get_cards(data))
            except (OSError, ValueError) as error:
                print("Could not import cards: " + str(error))
            else:
                data["cards"].extend(imported)
                storage.save_data(data)
                print("Imported " + str(len(imported)) + " cards.")
        else:
            print("Please pick a number from the menu.")


if __name__ == "__main__":
    main()
