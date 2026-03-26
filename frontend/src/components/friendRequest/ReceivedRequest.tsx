import { useFriendStore } from '@/stores/useFriendStore'
import React from 'react'
import FriendRequestItem from './FriendRequestItem';
import { Button } from '../ui/button';
import { toast } from 'sonner';

const ReceivedRequest = () => {
    const {acceptRequest, declineRequest, loading, receivedList} = useFriendStore();

    if (!receivedList || receivedList.length === 0) {
        return (
            <p className='text-sm text-muted-foreground'>
                No received request.
            </p>
        )
    }

    const handleAccept = async (requestId: string) => {
        try {
            await acceptRequest(requestId);
            toast.success("Accept request successfully")
        } catch (error) {
            console.error(error);
        }
    }

    const handleDecline = async (requestId: string) => {
        try {
            await declineRequest(requestId);
            toast.info("Request declined")
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <div className='space-y-3 mt-4'>
            {
                receivedList.map((req) => (
                    <FriendRequestItem 
                        key={req.id}
                        requestInfo={req}
                        actions={
                            <div className='flex gap-2'>
                                <Button className='rounded-md' size="sm" variant="primary" onClick={() => handleAccept(req.id)} disabled={loading}>
                                    Accept
                                </Button>
                                <Button className='rounded-md' size="sm" variant="destructiveOutline" onClick={() => handleDecline(req.id)} disabled={loading}>
                                    Decline
                                </Button>
                            </div>
                        }
                        type='received'
                    />
                ))
            }
        
        </div>
    )
}

export default ReceivedRequest
