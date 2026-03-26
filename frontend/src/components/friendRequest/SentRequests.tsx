import { useFriendStore } from '@/stores/useFriendStore'
import FriendRequestItem from './FriendRequestItem';

const SentRequests = () => {
    const {sentList} = useFriendStore();

    if (!sentList || sentList.length === 0) {
        return (
            <p className='text-sm text-muted-foreground'>
                No sent request.
            </p>
        )
    }

    return (
        <div className='space-y-3 mt-4'>
            <>{sentList.map((req) => (<FriendRequestItem key={req.id} requestInfo={req} type='sent' 
            actions={
                <p className='text-muted-foreground text-sm'>Waiting for replying</p>
            }/>))}</>
        </div>
    )
}

export default SentRequests
