def execution_tracer():
    print("[GENERATION] Starting")
    yield "A"

    print("[GENERATION] Resumed after A")
    yield "B"

    print("[GENERATION] Resumed after B -> Cleaning Up")


gen = execution_tracer()

print("Calling next(gen) 1st time:")
value_one = next(gen)
print(f"Got {value_one}")

# print("Calling next(gen) 2nd time:")
# value_two = next(gen)
# print(f"Got {value_two}")
