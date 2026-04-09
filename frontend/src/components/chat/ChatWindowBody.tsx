import { useChatStore } from "@/stores/useChatStore"
import ChatWelcomeScreen from "./ChatWelcomeScreen";
import MessageItem from "./MessageItem";
import { useLayoutEffect, useRef } from "react";
import InfiniteScroll from "react-infinite-scroll-component"

const ChatWindowBody = () => {
    const {activeConversationId, conversations, messages: allMessages, fetchMessages, fakeConversation} = useChatStore();

    const messages = allMessages[activeConversationId!]?.items ?? [];
    const reversedMessages = [...messages].reverse();
    const hasMore = allMessages[activeConversationId!]?.hasMore ?? false;
    const selectedConvo = conversations.find((c) => c.id === activeConversationId) ?? (fakeConversation ?? null);
    const key = `chat-scroll-${activeConversationId}`;

    const messagesEndRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    useLayoutEffect(() => {
        if (!messagesEndRef.current) {
            return;
        }

        messagesEndRef.current?.scrollIntoView({
            // behavior: "smooth",
            block: "end"
        });
    }, [activeConversationId])

    const fetchMoreMessages = async () => {
        if (!activeConversationId) {
            return;
        }
        
        try {
            await fetchMessages(activeConversationId);
        } catch (error) {
            console.error("Error while fetching messages", error);
        }
    }

    const handleScrollSave = () => {
        const container = containerRef.current;
        if (!container || !activeConversationId) {
            return;
        }

        sessionStorage.setItem(key, JSON.stringify({
            scrollTop: container.scrollTop,
            scrollHeight: container.scrollHeight,
        }))
    }

    useLayoutEffect(() => {
        const container = containerRef.current;
        if (!container) {
            return;
        }

        const item = sessionStorage.getItem(key);

        if (item) {
            const {scrollTop} = JSON.parse(item);

            requestAnimationFrame(() => {
                container.scrollTop = scrollTop;
            })
        }
    }, [messages.length])

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
            <div id="scrollableDiv" ref={containerRef} onScroll={handleScrollSave} className="flex flex-col-reverse overflow-y-auto overflow-x-hidden beautiful-scrollbar">
                <div ref={messagesEndRef}></div>

                <InfiniteScroll 
                    dataLength={messages.length} 
                    next={fetchMoreMessages} 
                    hasMore={hasMore} 
                    scrollableTarget="scrollableDiv"
                    loader={<p>Loading...</p>}
                    inverse={true}
                    style={{
                        display: "flex",
                        flexDirection: "column-reverse",
                        overflow: "visible"
                    }}
                >
                    {
                        reversedMessages.map((message, index) => (
                            <MessageItem 
                                key={message.id ?? index}
                                message={message}
                                index={index}
                                messages={reversedMessages}
                                selectedConvo={selectedConvo}
                            />
                        ))
                    }
                </InfiniteScroll>
            </div>
        </div>
    )
}

export default ChatWindowBody
