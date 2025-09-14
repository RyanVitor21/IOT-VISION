from supabase import create_client, Client

# 🔑 Substitua pelos valores do seu projeto Supabase
SUPABASE_URL = "https://jkrjjpvyxdkebilvqihk.supabase.co"
SUPABASE_KEY = ""

# Cria cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_to_supabase(total: int, inside: int, outside: int):
    """
    Envia os dados para a tabela people_counts no Supabase.
    Os campos 'id' e 'created_at' são gerados automaticamente no banco.
    """
    try:
        data = {
            "total_count": total,
            "inside_count": inside,
            "outside_count": outside
        }
        response = supabase.table("people_counts").insert(data).execute()

        if response.data:
            print("📡 Dados enviados para Supabase:", response.data)
        else:
            print("⚠️ Sem dados retornados, verifique a tabela ou as chaves.")

    except Exception as e:
        print("❌ Erro ao enviar para Supabase:", e)
