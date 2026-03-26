import { useEffect, useState, type Dispatch, type SetStateAction } from "react"
import {
    Dialog, DialogContent, DialogHeader, DialogTitle
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useFriendStore } from "@/stores/useFriendStore"
import SentRequests from "./SentRequests";
import ReceivedRequest from "./ReceivedRequest";

interface FriendRequestDialogProps {
    open: boolean;
    setOpen: Dispatch<SetStateAction<boolean>>;
}

const FriendRequestDialog = ({open, setOpen}: FriendRequestDialogProps) => {
    const [tab, setTab] = useState("received");
    const {getAllFriendRequests} = useFriendStore();

    useEffect(() => {
        const loadRequest = async () => {
            try {
                await getAllFriendRequests();
            } catch (error) {
                console.error("Error while loading requests", error);
            }
        }

        loadRequest();
    }, []);

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle>Invitation</DialogTitle>
                </DialogHeader>
                <Tabs value={tab} onValueChange={setTab} className="w-full grid">
                    <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="received" 
                            className="data-[state=active]:bg-white data-[state=active]:text-black"
                        >Received</TabsTrigger>
                        <TabsTrigger value="sent"
                            className="data-[state=active]:bg-white data-[state=active]:text-black"
                        >Sent</TabsTrigger>
                    </TabsList>

                    <TabsContent value="received">
                        <ReceivedRequest />
                    </TabsContent>

                    <TabsContent value="sent">
                        <SentRequests />
                    </TabsContent>
                </Tabs>
            </DialogContent>
        </Dialog>
    )
}

export default FriendRequestDialog
