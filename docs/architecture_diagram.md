digraph SystemArchitecture {
    graph [label="Архитектура бота days-afterX", fontsize=20, fontname="Arial", rankdir=TB, splines=ortho];
    node [shape=box, style="rounded,filled", fontname="Arial", fillcolor="#EFEFEF"];
    edge [fontname="Arial", fontsize=10];

    subgraph cluster_user {
        label = "Пользователь";
        style=dashed;
        user [label="Telegram-клиент"];
    }

    subgraph cluster_bot {
        label = "Бот";
        style=dashed;
        
        main [label="main.py / Dispatcher", fillcolor="#C9DAF8"];
        
        subgraph cluster_handlers {
            label = "Обработчики (Handlers)";
            common_handlers [label="common_handlers.py\n(public_router)"];
            event_handlers [label="event_handlers.py\n(private_router)"];
        }

        subgraph cluster_middlewares {
            label = "Прослойки (Middlewares)";
            auth_middleware [label="auth.py\n(AuthMiddleware)", fillcolor="#F4CCCC"];
        }
    }

    subgraph cluster_db {
        label = "База данных";
        style=dashed;
        database [label="PostgreSQL\n(Users, Events)", shape=cylinder];
    }

    // Связи
    user -> main [label=" /start, /add, ... "];
    main -> common_handlers;
    main -> event_handlers;
    
    event_handlers -> auth_middleware [label="Проверка\nдоступа", style=dashed, color=red, constraint=false];
    auth_middleware -> database [label="Запрос регистрации", style=dashed];

    common_handlers -> database [label="Регистрация", style=dashed];
    event_handlers -> database [label="Создание события", style=dashed];
}
