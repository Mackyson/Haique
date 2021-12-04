package handlers

import (
	"log"
	"net/http"

	"github.com/Mackyson/Haique/APIserver/models"
	"github.com/labstack/echo/v4"
)

const STRETCH_NUM = 5

// PostApiSignup -
func (c *Container) PostApiSignup(ctx echo.Context) error {
	var payload models.InlineObject1
	if err := (&echo.DefaultBinder{}).BindBody(ctx, &payload); err != nil {
		return err
	}
	name := payload.Name
	rawPw := payload.Pw

	hashedPw, err := hashPassword(rawPw, STRETCH_NUM)

	if err != nil {
		return err
	}
	session_id, err := genUUID()
	if err != nil {
		return err
	}
	/*
		{session_id}:linked_user_id -> {user_id}
		{name}:pw -> {pw}
		{name}:user_id -> {user_id}
	*/
	isNameUnique, err := c.RedisClient.SetNX(ctxBG, name+":pw", hashedPw, 0).Result()
	if err != nil {
		return err
	}
	if !isNameUnique {
		// 登録済みのuser名は不可
		tmp, err := c.RedisClient.Get(ctxBG, name+":pw").Result()
		log.Println(name, tmp, err)
		return ctx.NoContent(http.StatusConflict)
	}
	//pwは上でsetされていることに注意
	userId, err := c.RedisClient.Incr(ctxBG, "global:nextUserId").Result()
	if err != nil {
		return err
	}
	c.RedisClient.Set(ctxBG, name+":user_id", userId, 0)
	c.RedisClient.Set(ctxBG, session_id.String()+":linked_user_id", userId, 0)
	return ctx.JSON(http.StatusCreated, models.SessionId{Id: session_id})
}