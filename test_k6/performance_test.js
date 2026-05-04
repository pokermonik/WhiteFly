import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // Symulacja 20 użytkowników naraz przez 30 sekund
  vus: 20,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'], // Test nie przejdzie, jeśli >1% zapytań zawiedzie
    http_req_duration: ['p(95)<500'], // 95% zapytań musi być szybciej niż 500ms
  },
};

export default function () {
  //endpoint Flaska (Zadanie 1)
  let res1 = http.get('https://whitefly.onrender.com/flask/sync');
  check(res1, { 'status flask 200': (r) => r.status === 200 });

  let res1B = http.get('https://whitefly.onrender.com/flask/async');
  check(res1B, { 'status flask 200': (r) => r.status === 200 });

  //endpoint FastAPI (Zadanie 2)
  let res2 = http.get('https://whitefly.onrender.com/fastapi/sync');
  check(res2, { 'status fastapi 200': (r) => r.status === 200 });
  
  let res2B = http.get('https://whitefly.onrender.com/fastapi/async');
  check(res2B, { 'status fastapi 200': (r) => r.status === 200 });

  sleep(1);
}