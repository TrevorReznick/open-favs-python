import redis

#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX
#--kind python:default

class Config:
    
    REDIS_URL = "redis://vnavarra:UEJ8HnjTZSPr@redis:6379"
    REDIS_PREXIX = "vnavarra:"



def main(args):
    
    try:
        # Estrazione parametri Redis URL e prefisso
        redis_url = Config.REDIS_URL
        redis_prefix = Config.REDIS_PREXIX
        
        
        if not redis_url:
            
            return {"body": "Error: REDIS_URL is required and cannot be None"}
        
        # Connessione a Redis
        r = redis.from_url(redis_url)
        
        # Verifica se il server Redis è attivo
        if not r.ping():
            return {"body": "Error: Redis server not responding"}
        
        # Imposta e recupera il valore da Redis
        r.set(f"{redis_prefix}hello", "world")
        name = r.get(f"{redis_prefix}hello").decode()
        
        # Costruisce il messaggio di risposta
        greeting = f"Hello {name}!"
        return {"body": greeting}
    
    except Exception as e:
        return {"body": f"Error: {str(e)}"}

