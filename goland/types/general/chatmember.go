package general

type ChatMember struct {
	Status              string `json:"status"` // creator | administrator | member | restricted
	User                User   `json:"user"`
	CanBeEdited         bool   `json:"can_be_edited"`
	IsAnonymous         bool   `json:"is_anonymous"`
	CanManageChat       bool   `json:"can_manage_chat"`
	CanDeleteMessages   bool   `json:"can_delete_messages"`
	CanManageVideoChats bool   `json:"can_manage_video_chats"`
	CanRestrictMembers  bool   `json:"can_restrict_members"`
	CanPromoteMembers   bool   `json:"can_promote_members"`
	CanChangeInfo       bool   `json:"can_change_info"`
	CanInviteUsers      bool   `json:"can_invite_users"`
	CanPostStories      bool   `json:"can_post_stories"`
	CanEditStories      bool   `json:"can_edit_stories"`
	CanDeleteStories    bool   `json:"can_delete_stories"`

	CanPostMessages bool   `json:"can_post_messages,omitempty"`
	CanEditMessages bool   `json:"can_edit_messages,omitempty"`
	CanPinMessages  bool   `json:"can_pin_messages,omitempty"`
	CanManageTopics bool   `json:"can_manage_topics,omitempty"`
	CustomTitle     string `json:"custom_title,omitempty"`
}
