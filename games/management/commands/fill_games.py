from django.core.management.base import BaseCommand
from games.models import Genre, Company, Game
from datetime import datetime
import random

class Command(BaseCommand):
    help = 'Заполняет базу расширенным списком реальных игр'

    def handle(self, *args, **kwargs):
        # =========================================================================
        # ШАГ 1: СОЗДАНИЕ ЖАНРОВ
        # =========================================================================
        genres_data = [
            'Action', 'Adventure', 'RPG', 'Strategy', 'Shooter',
            'Sports', 'Racing', 'Puzzle', 'Simulation', 'Horror',
            'Fighting', 'Platformer', 'MMO', 'Indie', 'Open World',
            'Metroidvania', 'Survival', 'Roguelike', 'Visual Novel',
            'Survival Horror', 'Stealth', 'First-Person', 'Psychological',
            'Grand Strategy', 'Sandbox', 'Battle Royale', 'Cooperative'
        ]
        
        genres = {}
        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres[genre_name] = genre
            self.stdout.write(f'Создан жанр: {genre_name}')

        # =========================================================================
        # ШАГ 2: СОЗДАНИЕ КОМПАНИЙ (РАЗРАБОТЧИКИ И ИЗДАТЕЛИ)
        # =========================================================================
        companies_data = [
            # (name, description, is_developer, is_publisher)
            ('CD Projekt Red', 'Польский разработчик, известный по серии Ведьмак', True, False),
            ('CD Projekt', 'Польский издатель', False, True),
            ('Bethesda Game Studios', 'Американский разработчик The Elder Scrolls', True, False),
            ('Bethesda Softworks', 'Американский издатель', False, True),
            ('Rockstar Games', 'Разработчик GTA и Red Dead', True, True),
            ('Ubisoft', 'Французский разработчик и издатель', True, True),
            ('Electronic Arts', 'Американский издатель', False, True),
            ('BioWare', 'Канадский разработчик RPG', True, False),
            ('Nintendo', 'Японский разработчик и издатель', True, True),
            ('Sony Interactive Entertainment', 'Японский издатель', False, True),
            ('FromSoftware', 'Японский разработчик Dark Souls', True, False),
            ('Valve Corporation', 'Американский разработчик и издатель', True, True),
            ('Blizzard Entertainment', 'Американский разработчик', True, False),
            ('Square Enix', 'Японский разработчик и издатель', True, True),
            ('Capcom', 'Японский разработчик Resident Evil', True, False),
            
            # Новые компании для добавленных игр
            ('Team Cherry', 'Австралийский инди-разработчик Hollow Knight', True, True),
            ('Larian Studios', 'Бельгийский разработчик Baldur\'s Gate 3', True, True),
            ('Mojang Studios', 'Шведский разработчик Minecraft', True, False),
            ('Xbox Game Studios', 'Американский издатель', False, True),
            ('Bandai Namco', 'Японский издатель', False, True),
            ('Devolver Digital', 'Американский издатель инди-игр', False, True),
            ('Annapurna Interactive', 'Американский издатель арт-игр', False, True),
            
            # Компании для новых игр
            ('ZA/UM', 'Эстонская студия, разработчик Disco Elysium', True, True),
            ('Ice-Pick Lodge', 'Российский разработчик Pathologic', True, False),
            ('tinyBuild', 'Издатель инди-игр', False, True),
            ('11 bit studios', 'Польский разработчик и издатель Frostpunk', True, True),
            ('Mike Klubnika', 'Независимый разработчик Buckshot Roulette', True, True),
            ('Acid Wizard Studio', 'Польский инди-разработчик Darkwood', True, True),
            ('Arkane Studios', 'Французский разработчик Dishonored', True, False),
            ('Paradox Development Studio', 'Шведский разработчик стратегий', True, False),
            ('Paradox Interactive', 'Шведский издатель стратегических игр', False, True),
            ('Endnight Games', 'Канадский разработчик The Forest', True, True),
            ('Dontnod Entertainment', 'Французский разработчик Life is Strange', True, False),
            ('Nikita Kryukov', 'Российский инди-разработчик', True, True),
            ('Nolla Games', 'Финский разработчик Noita', True, True),
            ('Overkill Software', 'Шведский разработчик Payday', True, False),
            ('505 Games', 'Издатель Payday 2', False, True),
            ('PUBG Corporation', 'Корейский разработчик PUBG', True, False),
            ('Krafton', 'Корейский издатель PUBG', False, True),
            ('Rare', 'Британский разработчик Sea of Thieves', True, False),
            ('Firaxis Games', 'Американский разработчик Civilization', True, False),
            ('2K Games', 'Американский издатель Civilization', False, True),
            ('ConcernedApe', 'Американский разработчик Stardew Valley', True, True),
            ('Re-Logic', 'Американский разработчик Terraria', True, True),
            ('Giant Sparrow', 'Американский разработчик What Remains of Edith Finch', True, False),
        ]

        companies = {}
        for name, description, is_dev, is_pub in companies_data:
            company, created = Company.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            companies[name] = company
            self.stdout.write(f'Создана компания: {name}')

        # =========================================================================
        # ШАГ 3: СОЗДАНИЕ ИГР
        # =========================================================================
        real_games = [
            # (title, developer, publisher, release_year, genres, description)
            
            ('The Witcher 3: Wild Hunt', 'CD Projekt Red', 'CD Projekt', 2015, ['RPG', 'Open World', 'Adventure'], 'Эпическая RPG о ведьмаке Геральте'),
            ('Cyberpunk 2077', 'CD Projekt Red', 'CD Projekt', 2020, ['RPG', 'Open World', 'Shooter'], 'Научно-фантастическая RPG'),
            ('The Elder Scrolls V: Skyrim', 'Bethesda Game Studios', 'Bethesda Softworks', 2011, ['RPG', 'Open World'], 'Легендарная RPG с открытым миром'),
            ('Grand Theft Auto V', 'Rockstar Games', 'Rockstar Games', 2013, ['Action', 'Open World'], 'Криминальная сага в открытом мире'),
            ('Red Dead Redemption 2', 'Rockstar Games', 'Rockstar Games', 2018, ['Action', 'Open World', 'Adventure'], 'Приключения в диком западе'),
            ('Hollow Knight', 'Team Cherry', 'Team Cherry', 2017, ['Metroidvania', 'Action', 'Adventure', 'Platformer'], 'Исследуйте руины зараженного королевства насекомых'),
            ('Stardew Valley', 'ConcernedApe', 'ConcernedApe', 2016, ['Simulation', 'RPG', 'Indie'], 'Фермерская симуляция в пиксельном стиле'),
            ('Celeste', 'Maddy Makes Games', 'Maddy Makes Games', 2018, ['Platformer', 'Action', 'Indie'], 'Сложный платформер с глубокой историей'),
            ('Hades', 'Supergiant Games', 'Supergiant Games', 2020, ['Action', 'Roguelike', 'RPG', 'Indie'], 'Рогалик в мире греческой мифологии'),
            ('Undertale', 'Toby Fox', 'Toby Fox', 2015, ['RPG', 'Indie', 'Adventure'], 'Инновационная RPG где никто не должен умирать'),
            ('The Legend of Zelda: Breath of the Wild', 'Nintendo', 'Nintendo', 2017, ['Action', 'Adventure', 'Open World'], 'Новаторская игра серии Zelda'),
            ('Dark Souls III', 'FromSoftware', 'Bandai Namco', 2016, ['RPG', 'Action', 'Horror'], 'Сложная и атмосферная action-RPG'),
            ('Persona 5', 'Atlus', 'Atlus', 2016, ['RPG', 'Adventure'], 'Студенты-изгои, становящиеся ворами-призраками'),
            ('Final Fantasy VII Remake', 'Square Enix', 'Square Enix', 2020, ['RPG', 'Action', 'Adventure'], 'Ремейк культовой RPG'),
            ('Doom Eternal', 'id Software', 'Bethesda Softworks', 2020, ['Shooter', 'Action'], 'Беспощадный шутер против демонов'),
            ('Overwatch', 'Blizzard Entertainment', 'Blizzard Entertainment', 2016, ['Shooter', 'Action'], 'Командный шутер с уникальными героями'),
            ('Counter-Strike: Global Offensive', 'Valve Corporation', 'Valve Corporation', 2012, ['Shooter', 'Action'], 'Культовый тактический шутер'),
            ('The Last of Us Part II', 'Naughty Dog', 'Sony Interactive Entertainment', 2020, ['Action', 'Adventure', 'Horror'], 'Продолжение эмоциональной истории'),
            ('God of War', 'Santa Monica Studio', 'Sony Interactive Entertainment', 2018, ['Action', 'Adventure', 'RPG'], 'Переосмысление культовой серии'),
            ('Uncharted 4: A Thief\'s End', 'Naughty Dog', 'Sony Interactive Entertainment', 2016, ['Action', 'Adventure'], 'Приключения искателя сокровищ'),
            ('Baldur\'s Gate 3', 'Larian Studios', 'Larian Studios', 2023, ['RPG', 'Adventure', 'Strategy'], 'Глубокая RPG на основе D&D'),
            ('Elden Ring', 'FromSoftware', 'Bandai Namco', 2022, ['RPG', 'Action', 'Open World'], 'Открытый мир от создателей Dark Souls'),
            ('Animal Crossing: New Horizons', 'Nintendo', 'Nintendo', 2020, ['Simulation', 'Life', 'Indie'], 'Расслабляющая жизнь на острове'),
            ('Civilization VI', 'Firaxis Games', '2K Games', 2016, ['Strategy', 'Turn-Based'], 'Постройте величайшую империю'),
            ('The Sims 4', 'Maxis', 'Electronic Arts', 2014, ['Simulation', 'Life'], 'Симулятор жизни'),
            ('Cuphead', 'Studio MDHR', 'Studio MDHR', 2017, ['Action', 'Platformer', 'Indie'], 'Платформер в стиле 1930-х мультфильмов'),
            ('Dead Cells', 'Motion Twin', 'Motion Twin', 2018, ['Action', 'Roguelike', 'Metroidvania'], 'Рогалик-метроидвания'),
            ('Shovel Knight', 'Yacht Club Games', 'Yacht Club Games', 2014, ['Platformer', 'Action', 'Indie'], 'Ностальгический платформер'),
            ('Hollow Knight: Silksong', 'Team Cherry', 'Team Cherry', 2023, ['Metroidvania', 'Action', 'Platformer', 'Adventure'], 'Продолжение Hollow Knight с протагонистом Хорнет'),
            ('Disco Elysium', 'ZA/UM', 'ZA/UM', 2019, ['RPG', 'Detective', 'Indie'], 'Детективная RPG без боевой системы'),
            ('Pathologic 2', 'Ice-Pick Lodge', 'tinyBuild', 2019, ['Survival', 'Horror', 'RPG'], 'Переосмысление культовой российской игры о эпидемии'),
            ('Dota 2', 'Valve Corporation', 'Valve Corporation', 2013, ['MOBA', 'Strategy', 'Action'], 'Культовая multiplayer-игра в жанре MOBA'),
            ('Counter-Strike 2', 'Valve Corporation', 'Valve Corporation', 2023, ['Shooter', 'Action', 'First-Person'], 'Продолжение культового тактического шутера'),
            ('Frostpunk', '11 bit studios', '11 bit studios', 2018, ['Strategy', 'Survival', 'City-Builder'], 'Город-строитель в постапокалиптическом мире'),
            ('Frostpunk 2', '11 bit studios', '11 bit studios', 2024, ['Strategy', 'Survival', 'City-Builder'], 'Продолжение культовой стратегии о выживании'),
            ('Buckshot Roulette', 'Mike Klubnika', 'Mike Klubnika', 2023, ['Horror', 'Indie', 'Psychological'], 'Психологический хоррор с элементами рулетки'),
            ('Darkwood', 'Acid Wizard Studio', 'Acid Wizard Studio', 2017, ['Survival Horror', 'Indie', 'Top-Down'], 'Топ-даун хоррор выживания с процедурной генерацией'),
            ('Dishonored', 'Arkane Studios', 'Bethesda Softworks', 2012, ['Action', 'Stealth', 'Adventure'], 'Стелс-экшен с сверхспособностями в стимпанк-мире'),
            ('Dishonored 2', 'Arkane Studios', 'Bethesda Softworks', 2016, ['Action', 'Stealth', 'Adventure'], 'Продолжение культового стелс-экшена'),
            ('Hearts of Iron IV', 'Paradox Development Studio', 'Paradox Interactive', 2016, ['Strategy', 'Grand Strategy', 'Historical'], 'Гранд-стратегия о Второй мировой войне'),
            ('Europa Universalis IV', 'Paradox Development Studio', 'Paradox Interactive', 2013, ['Strategy', 'Grand Strategy', 'Historical'], 'Гранд-стратегия о мировой истории с 1444 по 1821 годы'),
            ('Europa Universalis V', 'Paradox Development Studio', 'Paradox Interactive', 2024, ['Strategy', 'Grand Strategy', 'Historical'], 'Новейшая часть серии гранд-стратегий'),
            ('The Forest', 'Endnight Games', 'Endnight Games', 2018, ['Survival', 'Horror', 'Adventure'], 'Хоррор на выживание на острове с каннибалами'),
            ('Life is Strange', 'Dontnod Entertainment', 'Square Enix', 2015, ['Adventure', 'Visual Novel', 'Drama'], 'Эмоциональная приключенческая игра о путешествиях во времени'),
            ('Milk inside a bag of milk inside a bag of milk', 'Nikita Kryukov', 'Nikita Kryukov', 2020, ['Visual Novel', 'Psychological', 'Indie'], 'Сюрреалистическая визуальная новелла о психическом здоровье'),
            ('Milk outside a bag of milk outside a bag of milk', 'Nikita Kryukov', 'Nikita Kryukov', 2021, ['Visual Novel', 'Psychological', 'Indie'], 'Продолжение сюрреалистической визуальной новеллы'),
            ('Noita', 'Nolla Games', 'Nolla Games', 2020, ['Roguelike', 'Action', 'Indie'], 'Рогалик с физикой на основе пикселей и магией'),
            ('PayDay 2', 'Overkill Software', '505 Games', 2013, ['Shooter', 'Action', 'Cooperative'], 'Кооперативный шутер о ограблениях'),
            ('PEAK', 'Unknown Developer', 'Unknown Publisher', 2021, ['Platformer', 'Indie', 'Adventure'], 'Инди-платформер о восхождении на гору'),
            ('Portal 2', 'Valve Corporation', 'Valve Corporation', 2011, ['Puzzle', 'Platformer', 'First-Person'], 'Культовая головоломка от Valve с порталами'),
            ('PUBG: Battlegrounds', 'PUBG Corporation', 'Krafton', 2017, ['Shooter', 'Battle Royale', 'Action'], 'Одна из первых и самых популярных игр в жанре королевской битвы'),
            ('Sea of Thieves', 'Rare', 'Xbox Game Studios', 2018, ['Adventure', 'Action', 'Open World'], 'Многопользовательское пиратское приключение в открытом мире'),
            ('Sid Meier\'s Civilization V', 'Firaxis Games', '2K Games', 2010, ['Strategy', 'Turn-Based', 'Historical'], 'Культовая пошаговая стратегия о развитии цивилизации'),
            ('Sid Meier\'s Civilization VI', 'Firaxis Games', '2K Games', 2016, ['Strategy', 'Turn-Based', 'Historical'], 'Продолжение легендарной серии стратегий'),
            ('Sid Meier\'s Civilization VII', 'Firaxis Games', '2K Games', 2025, ['Strategy', 'Turn-Based', 'Historical'], 'Предстоящая часть культовой серии стратегий'),
            ('Terraria', 'Re-Logic', 'Re-Logic', 2011, ['Sandbox', 'Adventure', 'Action'], '2D песочница с исследованием, крафтом и сражениями'),
            ('Victoria 2', 'Paradox Development Studio', 'Paradox Interactive', 2010, ['Strategy', 'Grand Strategy', 'Historical'], 'Гранд-стратегия о викторианской эпохе'),
            ('Victoria 3', 'Paradox Development Studio', 'Paradox Interactive', 2022, ['Strategy', 'Grand Strategy', 'Historical'], 'Современная гранд-стратегия о экономике и политике'),
            ('What Remains of Edith Finch', 'Giant Sparrow', 'Annapurna Interactive', 2017, ['Adventure', 'Walking Simulator', 'Drama'], 'Эмоциональная история о семье Финч и их проклятии'),
        ]

        # =========================================================================
        # ШАГ 4: СОЗДАНИЕ ОБЪЕКТОВ ИГР В БАЗЕ ДАННЫХ
        # =========================================================================
        for title, dev_name, pub_name, year, genre_names, description in real_games:
            # Находим или создаём разработчика
            developer = companies.get(dev_name)
            if not developer and dev_name not in ['Unknown Developer', 'Unknown Publisher']:
                developer, created = Company.objects.get_or_create(
                    name=dev_name,
                    defaults={'description': f'Разработчик игры {title}'}
                )
                companies[dev_name] = developer
            
            # Находим или создаём издателя
            publisher = companies.get(pub_name)
            if not publisher and pub_name not in ['Unknown Developer', 'Unknown Publisher']:
                publisher, created = Company.objects.get_or_create(
                    name=pub_name,
                    defaults={'description': f'Издатель игры {title}'}
                )
                companies[pub_name] = publisher

            # Пропускаем игру если нет разработчика или издателя
            if not developer or not publisher:
                self.stdout.write(f'❌ Пропущена игра {title} - компания не найдена')
                continue

            # Создаём или находим игру
            game, created = Game.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'developer': developer,
                    'publisher': publisher,
                    'release_date': datetime(year, random.randint(1, 12), random.randint(1, 28))
                }
            )
            
            # Добавляем жанры к игре
            game_genres = []
            for genre_name in genre_names:
                if genre_name in genres:
                    game_genres.append(genres[genre_name])
                else:
                    # Создаём жанр если его нет
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                    genres[genre_name] = genre
                    game_genres.append(genre)
            
            game.genres.set(game_genres)
            
            status = "✅ Создана" if created else "ℹ️ Уже существует"
            self.stdout.write(f'{status} игра: {title}')

        # =========================================================================
        # ШАГ 5: ВЫВОД СТАТИСТИКИ
        # =========================================================================
        self.stdout.write(
            self.style.SUCCESS('\n🎮 БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!')
        )
        
        self.stdout.write(f'📊 Статистика:')
        self.stdout.write(f'   • Игр: {Game.objects.count()}')
        self.stdout.write(f'   • Компаний: {Company.objects.count()}')
        self.stdout.write(f'   • Жанров: {Genre.objects.count()}')
        
        self.stdout.write(
            self.style.SUCCESS('\n✨ Теперь можно запускать сервер и проверять данные в админке!')
        )