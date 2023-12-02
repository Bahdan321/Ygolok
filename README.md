<h1>Для запуска app </h1>
    1. потребуеться создать .env файл пример можете найти
в env.template <br/>
2. запускаем docekr <br/>

```
    docker compose up --build
```
<br/>
3. заходим в pgadmin <br/>
4. создаем новый сервер: <br/>
<q>
Дальнейшие рекомендации сработают, если вы создали стандартный .env , который описан в env.template
</q>
<ul> 
<li>
Кликаем на Server -> Register
</li>
<li>
Появляется диалоговое окно вводим в поле Name произвольное имя
</li>
<li>
Переходим во вкладку Connection 
</li>
<li> 
в Host name/address пишем db_app 
</li>
<li>
username изменяем на postgres и пароль 1234
</li>
</ul>


<h2>для входа в pgadmin:<br/></h2>
login: noemail@noemail.com <br/>
password: 1234 <br/>
