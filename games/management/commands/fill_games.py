from django.core.management.base import BaseCommand
from games.models import Genre, Company, Game, Platform
from datetime import datetime
import random

class Command(BaseCommand):
    help = 'Заполняет базу играми, жанрами, компаниями и ПЛАТФОРМАМИ'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем заполнение базы данных...')

        # =========================================================================
        # ШАГ 1: СОЗДАНИЕ ЖАНРОВ
        # =========================================================================
        genres_data = [
            'Action', 'Adventure', 'RPG', 'Strategy', 'Shooter',
            'Sports', 'Racing', 'Puzzle', 'Simulation', 'Horror',
            'Fighting', 'Platformer', 'MMO', 'Indie', 'Open World',
            'Metroidvania', 'Survival', 'Roguelike', 'Visual Novel',
            'Survival Horror', 'Stealth', 'First-Person', 'Psychological',
            'Grand Strategy', 'Sandbox', 'Battle Royale', 'Cooperative',
            'Turn-Based', 'Detective', 'MOBA', 'City-Builder', 'Historical',
            'Walking Simulator', 'Drama'
        ]
        
        genres = {}
        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres[genre_name] = genre

        self.stdout.write(self.style.SUCCESS(f'✅ Жанры обработаны ({len(genres)} шт.)'))

        # =========================================================================
        # ШАГ 2: СОЗДАНИЕ КОМПАНИЙ
        # =========================================================================
        companies_data = [
            # (name, description)
            ('CD Projekt Red', 'Польский разработчик, Ведьмак и Cyberpunk'),
            ('CD Projekt', 'Польский издатель'),
            ('Bethesda Game Studios', 'Создатели TES и Fallout'),
            ('Bethesda Softworks', 'Издатель Bethesda'),
            ('Rockstar Games', 'Создатели GTA и RDR'),
            ('Ubisoft', 'Крупный французский издатель'),
            ('Electronic Arts', 'EA Sports и The Sims'),
            ('BioWare', 'Мастера RPG (Mass Effect, Dragon Age)'),
            ('Nintendo', 'Марио, Зельда и консоли'),
            ('Sony Interactive Entertainment', 'PlayStation Studios'),
            ('FromSoftware', 'Создатели жанра Souls-like'),
            ('Valve Corporation', 'Steam, Half-Life, Dota 2'),
            ('Blizzard Entertainment', 'Warcraft, Diablo, Overwatch'),
            ('Square Enix', 'Final Fantasy и JRPG'),
            ('Capcom', 'Resident Evil, Monster Hunter'),
            ('Team Cherry', 'Создатели Hollow Knight'),
            ('Larian Studios', 'Мастера CRPG, Baldur\'s Gate 3'),
            ('Mojang Studios', 'Создатели Minecraft'),
            ('Xbox Game Studios', 'Издатель Microsoft'),
            ('Bandai Namco', 'Японский издатель Dark Souls/Elden Ring'),
            ('Devolver Digital', 'Издатель крутых инди-игр'),
            ('Annapurna Interactive', 'Издатель атмосферных инди'),
            ('ZA/UM', 'Создатели Disco Elysium'),
            ('Ice-Pick Lodge', 'Российский геймдев, Мор (Утопия)'),
            ('tinyBuild', 'Издатель Hello Neighbor'),
            ('11 bit studios', 'Frostpunk и This War of Mine'),
            ('Mike Klubnika', 'Инди-разработчик'),
            ('Acid Wizard Studio', 'Создатели Darkwood'),
            ('Arkane Studios', 'Dishonored, Prey'),
            ('Paradox Development Studio', 'Гранд-стратегии'),
            ('Paradox Interactive', 'Издатель стратегий'),
            ('Endnight Games', 'The Forest'),
            ('Dontnod Entertainment', 'Life is Strange'),
            ('Nikita Kryukov', 'Инди-автор Milk outside a bag...'),
            ('Nolla Games', 'Создатели Noita'),
            ('Overkill Software', 'PayDay'),
            ('505 Games', 'Издатель'),
            ('PUBG Corporation', 'Battle Royale'),
            ('Krafton', 'Холдинг PUBG'),
            ('Rare', 'Sea of Thieves'),
            ('Firaxis Games', 'Civilization, XCOM'),
            ('2K Games', 'Издатель Bioshock, Civ, NBA'),
            ('ConcernedApe', 'Один человек - создатель Stardew Valley'),
            ('Re-Logic', 'Создатели Terraria'),
            ('Giant Sparrow', 'What Remains of Edith Finch'),
            ('Maddy Makes Games', 'Celeste'),
            ('Supergiant Games', 'Hades, Bastion'),
            ('Toby Fox', 'Undertale'),
            ('Atlus', 'Persona, SMT'),
            ('id Software', 'Doom, Quake'),
            ('Naughty Dog', 'Last of Us, Uncharted'),
            ('Santa Monica Studio', 'God of War'),
            ('Maxis', 'The Sims'),
            ('Studio MDHR', 'Cuphead'),
            ('Motion Twin', 'Dead Cells'),
            ('Yacht Club Games', 'Shovel Knight'),
        ]

        companies = {}
        for name, description in companies_data:
            company, created = Company.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            companies[name] = company
            
        self.stdout.write(self.style.SUCCESS(f'✅ Компании обработаны ({len(companies)} шт.)'))

        # =========================================================================
        # ШАГ 3: СОЗДАНИЕ ПЛАТФОРМ (НОВОЕ!)
        # =========================================================================
        platforms_data = [
            ('PC', 'Персональный компьютер (Windows, Linux, Mac)'),
            ('PlayStation 5', 'Консоль Sony текущего поколения'),
            ('PlayStation 4', 'Консоль Sony прошлого поколения'),
            ('Xbox Series X/S', 'Консоль Microsoft текущего поколения'),
            ('Xbox One', 'Консоль Microsoft прошлого поколения'),
            ('Nintendo Switch', 'Гибридная консоль Nintendo'),
        ]

        platforms = {}
        for name, desc in platforms_data:
            platform, created = Platform.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            platforms[name] = platform
            self.stdout.write(f'   + Платформа: {name}')

        self.stdout.write(self.style.SUCCESS('✅ Платформы созданы'))

        # =========================================================================
        # ШАГ 4: СПИСОК ИГР
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
            ('The Forest', 'Endnight Games', 'Endnight Games', 2018, ['Survival', 'Horror', 'Adventure'], 'Хоррор на выживание на острове с каннибалами'),
            ('Life is Strange', 'Dontnod Entertainment', 'Square Enix', 2015, ['Adventure', 'Visual Novel', 'Drama'], 'Эмоциональная приключенческая игра о путешествиях во времени'),
            ('Noita', 'Nolla Games', 'Nolla Games', 2020, ['Roguelike', 'Action', 'Indie'], 'Рогалик с физикой на основе пикселей и магией'),
            ('PayDay 2', 'Overkill Software', '505 Games', 2013, ['Shooter', 'Action', 'Cooperative'], 'Кооперативный шутер о ограблениях'),
            ('Portal 2', 'Valve Corporation', 'Valve Corporation', 2011, ['Puzzle', 'Platformer', 'First-Person'], 'Культовая головоломка от Valve с порталами'),
            ('PUBG: Battlegrounds', 'PUBG Corporation', 'Krafton', 2017, ['Shooter', 'Battle Royale', 'Action'], 'Одна из первых и самых популярных игр в жанре королевской битвы'),
            ('Sea of Thieves', 'Rare', 'Xbox Game Studios', 2018, ['Adventure', 'Action', 'Open World'], 'Многопользовательское пиратское приключение в открытом мире'),
            ('Sid Meier\'s Civilization V', 'Firaxis Games', '2K Games', 2010, ['Strategy', 'Turn-Based', 'Historical'], 'Культовая пошаговая стратегия о развитии цивилизации'),
            ('Terraria', 'Re-Logic', 'Re-Logic', 2011, ['Sandbox', 'Adventure', 'Action'], '2D песочница с исследованием, крафтом и сражениями'),
            ('Victoria 3', 'Paradox Development Studio', 'Paradox Interactive', 2022, ['Strategy', 'Grand Strategy', 'Historical'], 'Современная гранд-стратегия о экономике и политике'),
            ('What Remains of Edith Finch', 'Giant Sparrow', 'Annapurna Interactive', 2017, ['Adventure', 'Walking Simulator', 'Drama'], 'Эмоциональная история о семье Финч и их проклятии'),
        ]

        # =========================================================================
        # ШАГ 5: СОЗДАНИЕ ИГР И СВЯЗЫВАНИЕ
        # =========================================================================
        for title, dev_name, pub_name, year, genre_names, description in real_games:
            # 5.1 Компании
            developer = companies.get(dev_name)
            publisher = companies.get(pub_name)
            
            # Если компаний нет в словаре (на всякий случай, если кто-то добавил игру но не добавил компанию в список выше)
            if not developer:
                developer, _ = Company.objects.get_or_create(name=dev_name, defaults={'description': 'Разработчик'})
                companies[dev_name] = developer
            if not publisher:
                publisher, _ = Company.objects.get_or_create(name=pub_name, defaults={'description': 'Издатель'})
                companies[pub_name] = publisher

            # 5.2 Сама Игра
            game, created = Game.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'developer': developer,
                    'publisher': publisher,
                    'release_date': datetime(year, random.randint(1, 12), random.randint(1, 28))
                }
            )

            # 5.3 Жанры
            game_genres_objs = []
            for g_name in genre_names:
                # Если жанра вдруг нет, создадим
                if g_name not in genres:
                    g, _ = Genre.objects.get_or_create(name=g_name)
                    genres[g_name] = g
                game_genres_objs.append(genres[g_name])
            
            game.genres.set(game_genres_objs)

            # 5.4 ПЛАТФОРМЫ (УМНАЯ ЛОГИКА)
            game_platforms = []

            # Эксклюзивы Nintendo
            if pub_name == 'Nintendo':
                game_platforms.append(platforms['Nintendo Switch'])
            
            # Эксклюзивы Sony (PlayStation)
            elif pub_name == 'Sony Interactive Entertainment' or dev_name == 'Naughty Dog' or dev_name == 'Santa Monica Studio':
                if year >= 2020:
                    game_platforms.append(platforms['PlayStation 5'])
                game_platforms.append(platforms['PlayStation 4'])
                # Некоторые игры Sony вышли на ПК позже, добавим ПК
                if title in ['God of War', 'Horizon Zero Dawn', 'The Last of Us Part I', 'Uncharted 4: A Thief\'s End']:
                    game_platforms.append(platforms['PC'])
            
            # Остальные игры (обычно мультиплатформа)
            else:
                game_platforms.append(platforms['PC']) # Почти всё есть на ПК
                
                # Игры Xbox Game Studios есть на Xbox
                if pub_name == 'Xbox Game Studios' or dev_name == 'Rare' or dev_name == 'Bethesda Game Studios':
                    game_platforms.append(platforms['Xbox Series X/S'])
                    game_platforms.append(platforms['Xbox One'])

                # Обычная мультиплатформа (Ведьмак, ГТА и т.д.)
                else:
                    if year >= 2020:
                        game_platforms.append(platforms['PlayStation 5'])
                        game_platforms.append(platforms['Xbox Series X/S'])
                    
                    if year < 2023: # Старые консоли еще живы для игр до 2023
                        game_platforms.append(platforms['PlayStation 4'])
                        game_platforms.append(platforms['Xbox One'])
                    
                    # Инди игры часто есть на Свиче
                    if 'Indie' in genre_names:
                        game_platforms.append(platforms['Nintendo Switch'])

            # Применяем платформы
            game.platforms.set(game_platforms)
            
            status = "✅ Создана" if created else "🆗 Обновлена"
            self.stdout.write(f'{status}: {title} [{", ".join([p.name for p in game_platforms])}]')

        self.stdout.write(self.style.SUCCESS('\n✨ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!'))