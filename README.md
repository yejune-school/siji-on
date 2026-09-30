# 시지ON
시지중학교 학생용 비공식 포털.

## NEIS
GitHub Settings → Secrets and variables → Actions → Repository secrets에 `NEIS_API_KEY`를 추가합니다. Actions에서 `Update NEIS data`를 수동 실행할 수 있습니다.

## Pages
Settings → Pages → Source를 GitHub Actions로 설정합니다.

## Supabase
`config.js`에 anon/publishable key를 입력하고 `supabase.sql`을 실행하세요. service_role 키는 절대 넣지 마세요.
