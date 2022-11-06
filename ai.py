import os
import openai

openai.api_key = ("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")

response = openai.Completion.create(
  model="text-davinci-002",
  prompt="generate 5 SEO-friendly meta title that will rank better and get a higher CTR for the following details\n\nwebsite name: PALLET ANGLES\nwebsite url: https://www.tegral.com.au/product-category/load-protection/pallet-angles/\ntargeted keyword: load protection\n\n\n",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

#print('dawd')
print(response)

