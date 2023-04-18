package response

import (
	"fmt"
	"time"
)

type JsonTime uint64

func (j JsonTime) MarshalJSON() ([]byte, error) {
	var tmp = fmt.Sprintf("\"%s\"", time.Unix(int64(j), 0).Format("2006-01-02"))
	fmt.Printf("%s", tmp)
	return []byte(tmp), nil
}

type UserResponse struct {
	Id       int32    `json:"id,omitempty"`
	Mobile   string   `json:"mobile,omitempty"`
	NickName string   `json:"name,omitempty"`
	BirthDay JsonTime `json:"birthday,omitempty"`
	Gender   string   `json:"gender,omitempty"`
}
