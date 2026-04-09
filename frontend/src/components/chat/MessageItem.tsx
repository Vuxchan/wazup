import { cn, formatMessageTime } from "@/lib/utils";
import type { Conversation, Message, Participant } from "@/types/chat";
import UserAvatar from "./UserAvatar";
import { Card } from "../ui/card";
import SeenBadge from "./SeenBadge";

interface MessageItemProps {
    message: Message;
    index: number;
    messages: Message[];
    selectedConvo: Conversation;
}

const MessageItem = ({message, index, messages, selectedConvo}: MessageItemProps) => {
    const prev = index + 1 < messages.length ? messages[index + 1] : undefined;

    const isShowTime = index === 0 || new Date(message.createdAt).getTime() - new Date(prev?.createdAt || 0).getTime() > 300000;

    const isGroupBreak = isShowTime || message.senderId !== prev?.senderId; 
    
    const participant = selectedConvo.participants.find(
        (p: Participant) => p.id.toString() === message.senderId.toString()
    )

    const seenBy = selectedConvo.participants.filter((p) => selectedConvo.seenBy.includes(p.id))   
    
    return (
        <>
            <div className={cn("flex gap-2 mt-1", message.isOwn ? "justify-end" : "justify-start")}>
                {/* avatar */}
                {!message.isOwn && (
                    <div className="w-8">
                        {isGroupBreak && (
                            <UserAvatar 
                                type="chat"
                                name={participant?.displayName ?? "Wazup"}
                                avatarUrl={participant?.avatarUrl ?? undefined}
                            />
                        )}
                    </div>
                )}

                {/* messages */}
                <div className={cn("max-w-xs lg:max-w-md space-y-1 flex flex-col", message.isOwn ? "items-end" : "items-start")}>
                    <Card className={cn("p-3", message.isOwn ? "chat-bubble-sent border-0" : "chat-bubble-received")}>
                        <p className="text-sm leading-relaxed break-words">{message.content}</p>
                    </Card>

                    {/* seen/delivered */}
                    {
                        message.isOwn && message.id === selectedConvo.lastMessage?.id && (
                            <SeenBadge seenBy={seenBy}/>
                        )
                    }
                </div>
            </div>

            {/* time */}
            {isShowTime && (
                <span className="flex justify-center text-xs text-muted-foreground px-1">
                    {formatMessageTime(new Date(message.createdAt))}
                </span>
            )}
        </>
    )
}

export default MessageItem
