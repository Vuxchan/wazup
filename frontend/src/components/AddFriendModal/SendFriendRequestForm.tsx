import type { UseFormRegister } from "react-hook-form"
import type { IFormValues } from "../chat/AddFriendModal"
import { Label } from "../ui/label";
import { Textarea } from "../ui/textarea";
import { DialogFooter } from "../ui/dialog";
import { Button } from "../ui/button";
import { UserPlus } from "lucide-react";

interface SendRequestProps {
    register: UseFormRegister<IFormValues>;
    loading: boolean;
    searchedUsername: string;
    onSubmit?: (e: React.FormEvent<HTMLFormElement>) => void;
    onBack: () => void;
}

const SendFriendRequestForm = ({
    register, loading, searchedUsername, onSubmit, onBack
}: SendRequestProps) => {
  return (
    <form onSubmit={onSubmit}>
        <div className="space-y-4">
            <span className="success-message">
                Found <span className="font-semibold">@{searchedUsername}</span>
            </span>

            <div className="space-y-2">
                <Label htmlFor="message" className="text-sm font-semibold">
                    Enter greeting   
                </Label>
                <Textarea id="messasge" rows={3} placeholder="Hi! Let's be friend!"
                    className="glass border-border/50 focus:border-primary/50 transition-smooth resize-none"
                    {...register("message")}
                />
            </div>

            <DialogFooter>
                <Button type="button" variant="outline" className="flex-1 glass hover:text-destructive" onClick={onBack}>
                    Go back
                </Button>

                <Button type="submit" disabled={loading} 
                    className="flex-1 bg-gradient-chat text-white hover:opacity-90 transition-smooth"
                >
                    {loading ? (
                        <span>Sending...</span>
                    ) : (
                        <>
                            <UserPlus className="size-4 mr-2"/> Add friend
                        </>
                    )}
                </Button>
            </DialogFooter>
        </div>
    </form>
  )
}

export default SendFriendRequestForm
