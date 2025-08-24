<p align="center">
  <img src="https://www.theaiautomators.com/wp-content/uploads/2025/07/Group-2651.svg" alt="InsightsLM Logo" width="600"/>
</p>


# InsightsLM: The Open Source NotebookLM Alternative

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/theaiautomators/insights-lm-public?style=social)](https://github.com/theaiautomators/insights-lm-public/stargazers)
[![YouTube Video](https://img.shields.io/badge/YouTube-Watch%20the%20Build-red)](https://www.youtube.com/watch?v=IXJEGjfZRBE)

> What if the power of a tool like NotebookLM wasn't locked away in a closed system? What if you could build a private, self-hosted alternative that can be customized for your business needs, all without writing a single line of code?

That's exactly what we've done with **InsightsLM**. This project is an open-source, self-hostable alternative to NotebookLM. It's designed to be a powerful AI research tool that grounds its responses exclusively in the sources you provide, making it a reliable window into your company's knowledge base.


## About The Project

NotebookLM is one of the most powerful AI research tools available today. However, its closed-source nature limits its potential for customization and private hosting. InsightsLM was created to bridge this gap.

This isn't just a basic prototype. It's a robust application with some killer features, developed using a "vibe-coding" approach with Loveable for the Javascript frontend and a powerful backend combination of Supabase and N8N.

We are open-sourcing InsightsLM so you can install it, customize it, improve it, and even commercialize it. The ability to deploy AI agents grounded in a company's specific knowledge (a concept known as Retrieval-Augmented Generation or RAG) represents one of the biggest commercial opportunities for generative AI today.


<p align="center">
  <img src="https://www.theaiautomators.com/wp-content/uploads/2025/07/Group-2652.png" alt="The AI Automators Logo" width="500"/>
</p>


## Fully Local Version

This version of InsightsLM relies on cloud AI services like OpenAI and Gemini.

If you'd like to setup a fully local version of this that uses Ollama and Qwen3 along with Whisper and CoquiTTS, then check out our other repo below

[Fully Local InsightsLM](https://github.com/theaiautomators/insights-lm-local-package)

## Join Our Community

If you're interested in learning how to customize InsightsLM or build similar applications, join our community, The AI Automators.

https://www.theaiautomators.com/


## Key Features

* **Chat with Your Documents:** Upload your documents and get instant, context-aware answers.
* **Verifiable Citations:** Jump directly to the source of the information to ensure the AI isn't hallucinating.
* **Podcast Generation:** Create audio summaries and discussions from your source materials, just like in NotebookLM.
* **Private and Self-Hosted:** Maintain complete control over your data by hosting it yourself. Use local models if you wish.
* **Customizable and Extensible:** Built with modern, accessible tools, making it easy to tailor to your specific needs.


## Demo & Walkthrough

For a complete demonstration of InsightsLM, an overview of its architecture, and a step-by-step guide on how to set it up, check out our YouTube video:

<p>
  <a target="_blank" href="https://www.youtube.com/watch?v=IXJEGjfZRBE"><img src="https://raw.githubusercontent.com/theaiautomators/insights-lm-public/main/public/video.png" alt="Video" width="500"/></a>
</p>


## Built With

This project is built with a modern, powerful stack:
* **Frontend:** 
    * [Loveable](https://theaiautomators.com/go/loveable)
    * [Vite](https://vitejs.dev/)
    * [React](https://react.dev/)
    * [TypeScript](https://www.typescriptlang.org/)
    * [shadcn-ui](https://ui.shadcn.com/)
    * [Tailwind CSS](https://tailwindcss.com/)
* **Backend:**
    * [Supabase](https://supabase.com/) - for database, authentication, and storage.
    * [N8N](https://theaiautomators.com/go/n8n) - for workflow automation and backend logic.


## Getting Started: A Guide for No-Coders to Test and Customize

This guide provides the quickest way to get InsightsLM up and running so you can test, customize, and experiment.

I recommend you following along from 17:53 in our video here for the full step by step guide - [https://youtu.be/IXJEGjfZRBE?t=1073](https://youtu.be/IXJEGjfZRBE?t=1073)

You will need a notepad file open to copy and paste in various credentials and details.

1.  **Create Supabase Account and Project**
    * Go to [Supabase.com](https://supabase.com/) and create a free account.
    * Create a new project. Paste in your `database password` into your open notepad file as you will need this later.
2.  **Create GitHub Account & Repo from Template**
    * If you don't have one, create a free account on [GitHub](https://github.com/).
    * Navigate to the InsightsLM template repository here: [**github.com/theaiautomators/insights-lm-public**](https://github.com/theaiautomators/insights-lm-public)
    * Click the `Use this template` button to create a copy of the repository in your own GitHub account. Fill out the form.
3.  **Import into an AI-Coding Editor (Bolt.new)**
    * Create an account on [Bolt.new](https://bolt.new/) as it supports Supabase integration. (While the project was built on Loveable, it is currently quite difficult to import existing Github projects into Loveable)
    * Import your newly created GitHub repository into your Bolt project. You will need to link your Github account to Bolt. Choose the repo and import.
    * Now click Integrations on the top and connect your Supabase project. You will need to link your Supabase account to Bolt.
    * Once connected, the Supabase Edge Functions will auto-deploy. You will need to approve the running of the migration script to create the data structures in Supabase.
4.  **Import and Configure N8N Workflows**
    * The `/n8n` directory in this repository contains the JSON files for the required N8N workflows. There are 2 approaches here.
        1. The easiest is to import the "Import_Insights_LM_Workflows.json" file into a new workflow in n8n and follow the steps in the video. This includes configuring an n8n API key which will be used to auto-create all workflows needed by the system. You will also need to set various credentials.
        2. Instead of using the above workflow importer, you can instead download and import the 6 JSON workflows in this directory. You will need to go node by node in each workflow to configure them for your services. (e.g. Supabase, OpenAI, Gemini, Sub-Workflows etc). Follow the TODOs in each workflow.
5.  **Add N8N Webhooks to Supabase Secrets**
    * Your N8N workflows are triggered by webhooks from the Supabase Edge Functions. If you used the workflow importer, you will have the list of N8N secrets to create. Otherwise you'll need to gather these from the various workflows.
    * In your Supabase project dashboard, navigate to `Edge Functions` -> `Secrets` and add the following secrets. This allows the Supabase Edge Functions to securely call your N8N workflows.
    * These are the secrets that need to be created
        * NOTEBOOK_CHAT_URL
        * NOTEBOOK_GENERATION_URL
        * AUDIO_GENERATION_WEBHOOK_URL
        * DOCUMENT_PROCESSING_WEBHOOK_URL
        * ADDITIONAL_SOURCES_WEBHOOK_URL
        * NOTEBOOK_GENERATION_AUTH (This is the password for the custom Header Auth for each n8n Webhook)
        * OPENAI_API_KEY (This is used in the Generate Note Title edge function)
6.  **Test & Customize**
    * That's it! Your instance of InsightsLM should now be live.
    * You can now test the application, upload documents, and start chatting.
    * Within Bolt.new you can also deploy this to Netlify

## Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

- Fork the Project
- Create your Feature Branch (git checkout -b feature/AmazingFeature)
- Commit your Changes (git commit -m 'Add some AmazingFeature')
- Push to the Branch (git push origin feature/AmazingFeature)
- Open a Pull Request

## License

This codebase is distributed under the MIT License.

## A Note on n8n's Sustainable Use License

While InsightsLM is fully open-sourced and Supabase is also open source, it's important to be aware that n8n, which powers much of the backend automation, is not open source in the traditional sense.

n8n is distributed under a [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md). This license allows free usage for internal business purposes, including hosting workflows within your company or organization.

However, if you plan to use InsightsLM as part of a commercial SaaS offering—such as reselling access or hosting a public version for multiple clients—you may need to obtain an n8n Enterprise License. We’re not lawyers, so we recommend that you review the n8n license and contacting their team if your use case falls into a commercial category.

Alternatives: If your use case is restricted by the n8n license, one potential option is to convert key workflows into Supabase Edge Functions. This would allow you to fully avoid using n8n in production.