Własna konfiguracja serwera Apache `dostep.conf`.

Skrypt CGI napisany w Pyhton3 `uprawnienia.cgi`.

## Instrukcja uruchomienia

Polecenia należy wykonywać w głównym katalogu środowiska.

Budowa obrazu i uruchomienie kontenera
`docker compose up -d --build web`

Przykładowe żądania:
`curl.exe -i http://127.0.0.1:8080/`
`curl.exe -i -u student http://127.0.0.1:8080/` - poprosi o hasło 

Sprawdzanie logów:
`docker compose logs --tail 30 web`

Zatrzymanie środowiska:
`docker compose down`