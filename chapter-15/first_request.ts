import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY

const message = await client.messages.create({
  model: "claude-haiku-5-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "In one sentence, what is an API?" }],
});

for (const block of message.content) {
  if (block.type === "text") console.log(block.text);
}
console.log("Stop reason:", message.stop_reason);
