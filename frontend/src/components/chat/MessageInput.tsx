import { useAuthStore } from "@/stores/useAuthStore"
import { Button } from "../ui/button";
import { ImagePlus, Send } from "lucide-react";
import { Input } from "../ui/input";
import { useState } from "react";

const MessageInput = () => {
    const {user} = useAuthStore();
    const [value, setValue] = useState("");

    if (!user) return;

    return (
        <div className="flex items-center gap-2 p-3 min-h-[56px] bg-background">
            <Button variant="ghost" size="icon" className="hover:bg-primary/10 transition-smooth">
                <ImagePlus className="size-4"/>
            </Button>

            <div className="flex-1 relative">
                <Input value={value} onChange={(e) => setValue(e.target.value)}
                    placeholder="Texting..." className="pr-20 h-9 bg-white border-border/50 focus:border-primary/50 transition-smooth resize-none"
                ></Input>
                <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex items-center gap-1">
                    <Button asChild variant="ghost" size="icon"
                    className="size-8 hover:bg-primary/10 transition-smooth">
                        <div>
                            {/* emoji picker */}
                        </div>
                    </Button>
                </div>
            </div>
            <Button className="bg-gradient-chat hover:shadow-glow transition-smooth hover:scale-105" disabled={!value.trim()}>
                <Send className="size-4 text-white"/>
            </Button>
        </div>
    )
}

export default MessageInput
