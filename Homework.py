from pathlib import Path


def read_recipes(file_path: str | Path) -> dict:
    """Прочитать кулинарную книгу из файла.

    Args:
        file_path: путь к файлу с рецептами.

    Returns:
        Словарь вида {название блюда: [ингредиенты]}.
    """
    cook_book: dict = {}

    with open(file_path, encoding='utf-8') as file:
        while dish_name := file.readline().strip():
            ingredients_count = int(file.readline())
            ingredients = [
                _parse_ingredient(file.readline())
                for _ in range(ingredients_count)
            ]
            cook_book[dish_name] = ingredients
            file.readline()

    return cook_book


def _parse_ingredient(raw_line: str) -> dict:
    name, quantity, measure = (part.strip() for part in raw_line.split('|'))
    return {
        'ingredient_name': name,
        'quantity': int(quantity),
        'measure': measure,
    }


def get_shop_list_by_dishes(
    dishes: list[str],
    person_count: int,
    cook_book: dict,
) -> dict:
    """Сформировать список покупок для указанных блюд.

    Args:
        dishes: названия блюд из cook_book.
        person_count: количество персон.
        cook_book: словарь рецептов.

    Returns:
        Словарь {ингредиент: {'measure': ..., 'quantity': ...}}.
    """
    shop_list: dict = {}

    for dish in dishes:
        for ingredient in cook_book[dish]:
            name = ingredient['ingredient_name']
            portion = ingredient['quantity'] * person_count

            if name in shop_list:
                shop_list[name]['quantity'] += portion
            else:
                shop_list[name] = {
                    'measure': ingredient['measure'],
                    'quantity': portion,
                }

    return shop_list


def merge_files(file_paths: list[str | Path], result_path: str | Path) -> None:
    """Объединить текстовые файлы в один, отсортировав по числу строк.

    Перед содержимым каждого файла записываются его имя и количество строк.
    """
    contents = [(Path(path), _read_lines(path)) for path in file_paths]
    contents.sort(key=lambda item: len(item[1]))

    with open(result_path, 'w', encoding='utf-8') as result:
        for path, lines in contents:
            result.write(f'{path.name}\n{len(lines)}\n')
            for line in lines:
                result.write(line if line.endswith('\n') else line + '\n')

def _read_lines(file_path: str | Path) -> list[str]:
    with open(file_path, encoding='utf-8') as file:
        return file.readlines()


def main() -> None:
    cook_book = read_recipes('recipes.txt')

    shop_list = get_shop_list_by_dishes(
        ['Запеченный картофель', 'Омлет'], 2, cook_book
    )

    merge_files(['1.txt', '2.txt'], 'result.txt')


if __name__ == '__main__':
    main()