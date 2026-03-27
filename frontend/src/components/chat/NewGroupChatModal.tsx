import { useFriendStore } from "@/stores/useFriendStore";
import React, { useState } from "react"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "../ui/dialog";
import { User, UserPlus } from "lucide-react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import type { Friend } from "@/types/user";
import InviteSuggestionList from "../newGroupChat/InviteSuggestionList";
import SelectedUserList from "../newGroupChat/SelectedUserList";
import { toast } from "sonner";
import { useChatStore } from "@/stores/useChatStore";
import { Button } from "../ui/button";


const NewGroupChatModal = () => {
    const [groupName, setGroupName] = useState("");
    const [search, setSearch] = useState("");
    const {friends, getFriends} = useFriendStore();
    const [invitedUsers, setInvitedUsers] = useState<Friend[]>([])
    const {createConversation, loading} = useChatStore();

    const handleGetFriends = async () => {
        await getFriends();
    }

    const handleSelectFriend = (friend: Friend) => {
        setInvitedUsers([...invitedUsers, friend]);
        setSearch("");
    }

    const handleRemoveFriend = (friend: Friend) => {
        setInvitedUsers(invitedUsers.filter((u) => u.id !== friend.id));
    }

    const handleSubmit = async (e: React.FormEvent) => {
        try {
            e.preventDefault();
            if (invitedUsers.length < 2) {
                toast.warning("You must invite at least 2 user");
                return;
            }

            await createConversation(
                "group",
                groupName,
                invitedUsers.map((u) => u.id)
            );

            handleCancel();
        } catch (error) {
            console.error("Error while handling submit in NewGroupChatModal", error);
        }
    }

    const filterFriends = friends.filter((friend) => friend.displayName.toLocaleLowerCase().includes(search.toLocaleLowerCase()) && !invitedUsers.some((u) => u.id === friend.id))

    const handleCancel = () => {
        setGroupName("");
        setSearch("");
        setInvitedUsers([]);
    }

    return (
        <Dialog onOpenChange={handleCancel}>
            <DialogTrigger asChild onClick={handleGetFriends}>
                <div className="flex justify-center items-center size-5 rounded-full hover:bg-sidebar-accent cursor-pointer z-10">
                    <User className="size-4"/>
                    <span className="sr-only">Create group</span>
                </div>
            </DialogTrigger>

            <DialogContent className="sm:max-w-[425px] border-none">
                <DialogHeader>
                    <DialogTitle className="capitalize">Create new group chat</DialogTitle>
                </DialogHeader>

                <form className="space-y-4" onSubmit={handleSubmit}>
                    {/* Group name */}
                    <div className="space-y-2">
                        <Label htmlFor="groupName" className="text-sm font-semibold">Group name</Label>
                        <Input id="groupName" placeholder="Type group name..." 
                            className="glass border-border/50 focus:border-primary/50 transition-smooth"
                            value={groupName}
                            onChange={(e) => setGroupName(e.target.value)}
                            required
                        />
                    </div>

                    {/* Invite */}
                    <div className="space-y-2">
                        <Label htmlFor="invite" className="text-sm font-semibold">
                            Invite member
                        </Label>

                        <Input id="invite" placeholder="Search by display name..." value={search} onChange={(e) => setSearch(e.target.value)}/>

                        {search && filterFriends.length > 0 && <InviteSuggestionList filterFriends={filterFriends} onSelect={handleSelectFriend}/>}

                        <SelectedUserList invitedUsers={invitedUsers} onRemove={handleRemoveFriend}/>

                    </div>

                    <DialogFooter>
                        <Button type="submit" disabled={loading} 
                            className="flex-1 bg-gradient-chat text-white hover:opacity-90 transition-smooth"
                        >
                            {
                                loading ? (
                                    <span>Creating...</span>
                                ) : (
                                    <>
                                        <UserPlus className="size-4 mr-2"/>
                                        Create group
                                    </>
                                )
                            }    
                        </Button>    
                    </DialogFooter> 
                </form>
            </DialogContent>
        </Dialog>
    )
}

export default NewGroupChatModal
