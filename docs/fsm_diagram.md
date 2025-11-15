digraph FSM_AddEvent {
    rankdir=LR;
    node [shape=box, style=rounded, fontname="Arial"];
    edge [fontname="Arial", fontsize=10];

    // Узел для начального и конечного состояний
    __initial__ [label="", shape=circle, style=filled, fillcolor=black, width=0.25];
    __final__ [label="", shape=doublecircle, style=filled, fillcolor=black, width=0.25];

    // Состояния
    Idle [label="Ожидание\nкоманды"];
    WaitingName [label="Ожидание имени\n(AddEvent.waiting_for_name)"];
    WaitingDate [label="Ожидание даты\n(AddEvent.waiting_for_date)"];

    // Переходы
    __initial__ -> Idle;

    Idle -> WaitingName [label="/add (пустой)"];
    Idle -> __final__ [label="/add [название] [дата]\n(быстрый путь)"];
    
    WaitingName -> WaitingDate [label="Ввод текста (название)"];
    WaitingName -> __final__ [label="Нажатие 'Отмена'"];

    WaitingDate -> __final__ [label="Ввод корректной даты\n(текст или кнопка)"];
    WaitingDate -> WaitingDate [label="Ввод неверной даты"];
    WaitingDate -> __final__ [label="Нажатие 'Отмена'"];

    __final__ -> Idle [style=dashed, arrowhead=none];
}
