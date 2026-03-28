import { NavUser } from "@/components/sidebar/nav-user"
import {
Sidebar,
SidebarContent,
SidebarFooter,
SidebarGroup,
SidebarGroupAction,
SidebarGroupContent,
SidebarGroupLabel,
SidebarHeader,
SidebarMenu,
SidebarMenuButton,
SidebarMenuItem,
} from "@/components/ui/sidebar"
import { Moon, Sun } from "lucide-react"
import { Switch } from "../ui/switch"
import CreateNewChat from "../chat/CreateNewChat"
import NewGroupChatModal from "../chat/NewGroupChatModal"
import GroupChatList from "../chat/GroupChatList"
import AddFriendModal from "../chat/AddFriendModal"
import DirectMessageList from "../chat/DirectMessageList"
import { useThemeStore } from "@/stores/useThemeStore"
import { useAuthStore } from "@/stores/useAuthStore"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
    const {isDark, toggleTheme} = useThemeStore();
    const {user} = useAuthStore();

    return (
        <Sidebar variant="inset" {...props}>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton size="lg" asChild className="bg-gradient-primary">
                        <a href="#">
                            <div className="flex w-full items-center px-2 justify-between">
                            <h1 className="text-xl font-bold text-white">
                                Wazup
                            </h1>
                            <div className="flex items-center gap-2">
                                <Sun className="size-4 text-white/80"/>
                                <Switch 
                                checked={isDark}
                                onCheckedChange={toggleTheme} 
                                className="data-[state=checked]:bg-background/80"
                                />
                                <Moon className="size-4 text-white/80"/>
                            </div>
                            </div>
                        </a>

                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent className="beautiful-scrollbar">
                {/* New Chat */}
                <SidebarGroup>
                    <SidebarGroupContent>
                        <CreateNewChat />
                    </SidebarGroupContent>
                </SidebarGroup>

                {/* Group Chat */}
                <SidebarGroup>
                    <SidebarGroupLabel className="uppercase">
                        group chat
                    </SidebarGroupLabel>
                    <SidebarGroupAction title="Create Group" className="cursor-pointer">
                        <NewGroupChatModal />
                    </SidebarGroupAction>

                    <SidebarGroupContent>
                        <GroupChatList />
                    </SidebarGroupContent>
                </SidebarGroup>

                {/* Direct Message */}
                <SidebarGroup>
                    <SidebarGroupLabel className="uppercase">
                        friends
                    </SidebarGroupLabel>
                    <SidebarGroupAction title="Add Friend" className="cursor-pointer">
                        <AddFriendModal />
                    </SidebarGroupAction>

                    <SidebarGroupContent>
                        <DirectMessageList />
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter>
                {user && <NavUser user={user} />}
            </SidebarFooter>
        </Sidebar>
    )
}
