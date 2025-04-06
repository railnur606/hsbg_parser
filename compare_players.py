import pandas as pd


def find_player_rankings():
    try:
        full_ranking = pd.read_excel('data/hs_bg_api_leaderboard_async.xlsx')
        players_list = pd.read_excel('data/players_list.xlsx')

        if 'battleTagName' not in players_list.columns:
            raise ValueError("Файл с игроками должен содержать столбец 'battleTagName'")


        full_ranking['Player_norm'] = full_ranking['Player'].str.lower().str.strip()
        players_list['battleTagName_norm'] = players_list['battleTagName'].str.lower().str.strip()

        result = players_list.merge(
            full_ranking,
            how='left',
            left_on='battleTagName_norm',
            right_on='Player_norm'
        )

        result = result.rename(columns={
            'Rank': 'Позиция в рейтинге',
            'Rating': 'Рейтинг'
        })[['battleTagName', 'Позиция в рейтинге', 'Рейтинг']]

        result.to_excel('data/players_ranking_results.xlsx', index=False)

        matched = result['Позиция в рейтинге'].notna().sum()
        print(f"Успешно сопоставлено: {matched} из {len(players_list)} игроков")
        if matched < len(players_list):
            print("Не найдены в рейтинге:")
            print(result[result['Позиция в рейтинге'].isna()]['battleTagName'].to_string(index=False))

        return True

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False


if __name__ == "__main__":
    if find_player_rankings():
        print("Результаты успешно сохранены в players_ranking_results.xlsx")
    else:
        print("Произошла ошибка при обработке данных")
