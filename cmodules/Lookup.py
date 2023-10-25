import ast

def Lookup(s, MAX_LINE, request_queue, response_queue):
    pokemon = input("Search for pokemon on name: ")
    request = f"LOOKUP {pokemon}\n"
    request_queue.put(request)
    response = ast.literal_eval(response_queue.get())
    
    if "400" in response or "401" in response or "404" in response:
        print("No pokemon records found.")
        return
    else:
        print("Pokemon records found:", response)
        
    
__all__ = ["Lookup"]