import { useFriendStore } from '@/stores/useFriendStore'
import { DialogContent, DialogHeader, DialogTitle } from '../ui/dialog';
import { MessageCircleMore, User } from 'lucide-react';
import { Card } from '../ui/card';
import UserAvatar from '../chat/UserAvatar';
import { useChatStore } from '@/stores/useChatStore';

const FriendListModal = () => {
    const {friends} = useFriendStore();
    const {createConversation} = useChatStore();

    const handleAddConversation = async (friendId: string) => {
        await createConversation("direct", "", [friendId]);
    }

    return (
        <DialogContent className='glass max-w-md'>
            <DialogHeader>
                <DialogTitle className='flex items-center gap-2 text-xl capitalize'>
                    <MessageCircleMore className='size-5'/>
                    Start a new conversation
                </DialogTitle>
            </DialogHeader>

            {/* friends list */}
            <div className='space-y-4'>
                <h1 className='text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-white'>
                    Friend list
                </h1>

                <div className='space-y-2 mmax-h-50 overflow-y-auto'>
                    {friends.map((friend) => (
                        <Card key={friend.id}
                            onClick={() => handleAddConversation(friend.id)}
                            className='p-3 cursor-pointer transition-smooth hover:shadow-soft glass hover:bg-muted/30 group/friendCard'
                        >
                            <div className='flex items-center gap-3'>
                                {/* avatar */}
                                <div className='relative'>
                                    <UserAvatar 
                                        type='sidebar'
                                        name={friend.displayName}
                                        avatarUrl={friend.avatarUrl}
                                    />
                                </div>

                                {/* info */}
                                <div className='flex-1 min-w-0 flex flex-col'>
                                    <h2 className='font-semibold text-sm truncate'>
                                        {friend.displayName}
                                    </h2>
                                    <span className='text-sm text-muted-foreground'>@{friend.username}</span>
                                </div>
                            </div>
                        </Card>
                    ))}

                    {friends.length === 0 && (
                        <div className='text-center py-8 text-muted-foreground'>
                            <User className='size-12 mx-auto mb-3 opacity-50'/>
                            Don't have friend. Connect and start a new conversation!
                        </div>
                    )}
                </div>
            </div>
        </DialogContent>
    )
}

export default FriendListModal
