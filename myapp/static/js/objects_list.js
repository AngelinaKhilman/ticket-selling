ymaps.ready(init);

function init() {

    // Создание экземпляра карты.
    var myMap = new ymaps.Map('map', {
            center: [50.443705, 30.530946],
            zoom: 14
        }, {
            searchControlProvider: 'yandex#search'
        }),
        // Контейнер для меню.
        menu = $('<ul class="menu"/>');

    for (var i = 0, l = groups.length; i < l; i++) {
        createMenuGroup(groups[i]);
    }

    function createMenuGroup (group) {
        // Пункт меню.
        var menuItem = $('<li><a1 href="#" style="color: #656565; font-size: 18pt; font-family: Helvetica, sans-serif">' + group.name + '</a1></li>'),
        // Коллекция для геообъектов группы.
            collection = new ymaps.GeoObjectCollection(null, { preset: group.style }),
        // Контейнер для подменю.
            submenu = $('<ul class="submenu"/>');

        // Добавляем коллекцию на карту.
        myMap.geoObjects.add(collection);
        // Добавляем подменю.
        menuItem
            .append(submenu)
            // Добавляем пункт в меню.
            .appendTo(menu)
            // По клику удаляем/добавляем коллекцию на карту и скрываем/отображаем подменю.
            .find('a1')
            .bind('click', function () {
                if (collection.getParent()) {
                    myMap.geoObjects.remove(collection);
                    submenu.hide();
                } else {
                    myMap.geoObjects.add(collection);
                    submenu.show();
                }
            });
            submenu.hide();
        for (var j = 0, m = group.items.length; j < m; j++) {
            createSubMenu(group.items[j], collection, submenu);
        }
    }

    function createSubMenu (item, collection, submenu) {
        // Пункт подменю.
        var submenuItem1 = $('<li><a1 href="#" style="color: #656565; font-size: 14pt; font-family: Helvetica, sans-serif">' + item.name + '</a1></li>'),
            submenuItem2 = $('<li><a1 href="#" style="color: #656565; font-size: 11pt; font-family: Helvetica, sans-serif"> Address: ' + item.address + '</a1></li>'),
            submenuItem3 = $('<li><a1 href="#" style="color: #656565; font-size: 11pt; font-family: Helvetica, sans-serif"> Phone: ' + item.phone + '</a1></li>'),
            submenuItem4 = $('<li><a1 href="#" style="color: #656565; font-size: 11pt; font-family: Helvetica, sans-serif"> Work time: ' + item.work_time + '</a1></li>'),
        // Создаем метку.
            placemark = new ymaps.Placemark(item.center, { balloonContent: item.address });

        // Добавляем метку в коллекцию.
        collection.add(placemark);
        // Добавляем пункт в подменю.
        submenuItem1
            .appendTo(submenu)
            // При клике по пункту подменю открываем/закрываем баллун у метки.
            .find('a1')
            .bind('click', function () {
                if (!placemark.balloon.isOpen()) {
                    placemark.balloon.open();
                } else {
                    placemark.balloon.close();
                }
                return false;
            });

        submenuItem2
            .appendTo(submenu);
        submenuItem3
            .appendTo(submenu);
        submenuItem4
            .appendTo(submenu);

    }

    // Добавляем меню в тэг BODY.
    menu.appendTo($('.con4'));
    // Выставляем масштаб карты чтобы были видны все группы.
    myMap.setBounds(myMap.geoObjects.getBounds());
}