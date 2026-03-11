const defaultConfig = {
  theme: {
    colorPrimary: "#615CED",
    darkMode: false,
    prefix: "test_with_ai",
    leftHeader: {
      logo: "",
      title: "Work with Test with AI",
    },
  },
  sender: {
    attachments: false,
    maxLength: 10000,
    disclaimer: "Works for you, grows with you",
  },
  welcome: {
    greeting: "Hello, how can I help you today?",
    description:
      "I am a helpful assistant that can help you with your questions.",
    avatar: `${import.meta.env.BASE_URL}test_with_ai-symbol.svg`,
    prompts: [
      {
        value: "Let's start a new journey",
      },
      {
        value: "Can you tell me what skills you have?",
      },
    ],
  },
  api: {
    baseURL: "",
    token: "",
  },
} as const;

export default defaultConfig;

export type DefaultConfig = typeof defaultConfig;
