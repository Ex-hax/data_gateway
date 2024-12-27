DO
$$
BEGIN
   -- Check if the user 'admin' exists
   IF NOT EXISTS (
      SELECT id FROM public.user WHERE user_name = 'admin' OR id = 1
   ) THEN
      -- Create the 'admin' user if it does not exist
      INSERT INTO public.user ("uuid", user_name, password, email, mobile_phone) 
      VALUES (gen_random_uuid(), 'admin', '{{params.password}}', 'admin@mail.com', '0999999999');
   ELSE
      -- Update the password for the existing 'admin' user
      UPDATE public.user
      SET password = '{{params.password}}'
      WHERE user_name = 'admin' OR id = 1;
   END IF;
END
$$;
