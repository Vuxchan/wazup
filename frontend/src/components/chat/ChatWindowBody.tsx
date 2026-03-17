import { useChatStore } from "@/stores/useChatStore"
import ChatWelcomeScreen from "./ChatWelcomeScreen";
import MessageItem from "./MessageItem";

const ChatWindowBody = () => {
    const {activeConversationId, conversations, messages: allMessages} = useChatStore();

    const messages = allMessages[activeConversationId!]?.items ?? [];
    const selectedConvo = conversations.find((c) => c.id === activeConversationId);

    if (!selectedConvo) {
        return <ChatWelcomeScreen />
    }

    if (!messages?.length) {
        return (
            <div className="flex h-full items-center justify-center text-muted-foreground">
                Conversation has no message
            </div>
        )
    }

    return (
        <div className="p-4 bg-primary-foreground h-full flex flex-col overflow-hidden">
            <div className="flex flex-col overflow-y-auto overflow-x-hidden beautiful-scrollbar">
                {
                    messages.map((message, index) => (
                        <MessageItem 
                            key={message.id ?? index}
                            message={message}
                            index={index}
                            messages={messages}
                            selectedConvo={selectedConvo}
                            lastMessageStatus="delivered"
                        />
                    ))
                }
            </div>
        </div>
    )
}

export default ChatWindowBody
