import type { Participant } from "@/types/chat"
import { Badge } from "../ui/badge"
import UserAvatar from "./UserAvatar";

const SeenBadge = ({seenBy}: {seenBy: Participant[]}) => {
    const avatars = [];
    const limit = Math.min(seenBy.length, 3);

    for (let i = 0; i < limit; i++) {
        const member = seenBy[i];
        avatars.push(
            <UserAvatar key={member.id} type="seen" name={member.displayName} avatarUrl={member.avatarUrl ?? undefined}/>
        )
    }

    if (seenBy.length === 0) {
        return (
            <Badge variant="outline" className="text-xs px-1.5 py-0.5 h-4 border-0 bg-muted text-muted-foreground">delivered</Badge>
        )  
    }
    else if (seenBy.length <= 3) {
        return (
            <div className="relative flex -space-x-2 *:data-[slot=avatar]:ring-background *data-[slot=avatar]:ring-2">
                {avatars}
            </div>
        )
    }
    else if (seenBy.length <= 10) {
        return (
            <div className="flex items-center">
                <div className="relative flex -space-x-2 *:data-[slot=avatar]:ring-background *data-[slot=avatar]:ring-2">
                    {avatars}
                </div>
                <Badge variant="outline" className="text-xs px-1.5 py-0.5 h-4 border-0 bg-primary/20 text-primary">+{seenBy.length - limit}</Badge>
            </div>
        )
    }

    return (
        <div>
            <Badge variant="outline" className="text-xs px-1.5 py-0.5 h-4 border-0 bg-primary/20 text-primary">seen by {seenBy.length} people</Badge>
        </div>
    )
}

export default SeenBadge
