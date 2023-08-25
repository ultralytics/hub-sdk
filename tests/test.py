from hub_client import HUBClient

# Authenticate with the server
# crednetials = {"api_key": "0cfff8f4e9357c3777c0871d35802915913c2f71c3"}
crednetials = {"email": "rick.sanchez@citadel.com", "password": "987654321"}
client = HUBClient(crednetials)

model_list = client.model_list(page_size=1)  # Use client.ModelList to create an instance
print("1: ", model_list.results)
model_list.next()
print("2: ", model_list.results)
model_list.previous()
print("previous: ", model_list.results)


# model = client.model({"meta":{"name":"my Model"}})
# print(model.data)

# model = client.model("KUGRLIK8C4nytMcYNiW9")
# print(model.update({"meta": {"name": "Model Name"}}))





# Upload a model
# response = models.upload("MODEL_ID", "CKPT", {"meta": "args"})
# # Predict with a model
# response = models.predict("MODEL_ID", "IMAGE", {"config": "args"})
# # Export a model
# response = models.export("MODEL_ID", {"format": "name"})


# Response is returned in this format
response = {
    "success": "true or false, for developers who are not familiar with status codes",
    "message": "Summary of result",
    "data": "Nested JSON with the result or an empty object if not needed.",
}

# Coming Soon

# Cloud training
# response = models.train("MODEL_ID", {"config": "args"})
