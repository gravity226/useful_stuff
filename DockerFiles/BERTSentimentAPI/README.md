## Build it
docker build -t sentiment-api .

## Run it
docker run -p 8000:8000 sentiment-api

## Test
- curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Evolv Technologies (EVLV) Soars 5.8%: Is Further Upside Left in the Stock?"}'

- curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Strength Seen in Nektar (NKTR): Can Its 12.1% Jump Turn into More Strength?"}'

- curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Stem Appoints New Chief Financial Officer"}'