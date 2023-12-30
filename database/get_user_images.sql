SELECT U.Username, G.ImageLink, G.TimeCreated, G.Caption, G.Prompt
        FROM GeneratedImages G
        INNER JOIN Users U on G.UserID = U.UserID
        WHERE U.Username = 'chndlr';